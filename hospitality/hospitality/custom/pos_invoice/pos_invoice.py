import frappe
from frappe.utils import nowdate
import json

@frappe.whitelist()
def sell_on_credit(invoice_data):
	
	invoice_data = json.loads(invoice_data)

	if not invoice_data.get("customer") or not invoice_data.get("items"):
		frappe.throw("Customer and Items are required.")

	warehouse = None
	if invoice_data.get("pos_profile"):
		warehouse = frappe.db.get_value("POS Profile", invoice_data["pos_profile"], "warehouse")
	
	sales_invoice = frappe.new_doc("Sales Invoice")
	sales_invoice.customer = invoice_data["customer"]
	sales_invoice.due_date = nowdate()
	sales_invoice.selling_price_list = "Standard Selling"
	sales_invoice.is_pos = 0
	sales_invoice.update_stock = 1

	for item in invoice_data["items"]:
		sales_invoice.append("items", {
			"item_code": item["item_code"],
			"qty": item["qty"],
			"rate": item["rate"],
			"uom": item["uom"],
			"conversion_factor": item["conversion_factor"],
			"warehouse": warehouse,
		})

	if invoice_data.get("taxes_and_charges"):
		sales_invoice.taxes_and_charges = invoice_data["taxes_and_charges"]
	
	# if invoice_data.get("taxes"):
	# 	for tax in invoice_data["taxes"]:
	# 		sales_invoice.append("taxes", {
	# 			"charge_type": tax.get("charge_type"),
	# 			"account_head": tax.get("account_head"),
	# 			"description": tax.get("description"),
	# 			"rate": tax.get("rate"),
	# 			"cost_center": tax.get("cost_center"),
	# 			"tax_amount": tax.get("tax_amount"),
	# 			"tax_amount_after_discount_amount": tax.get("tax_amount_after_discount_amount"),
	# 			"base_tax_amount": tax.get("base_tax_amount"),
	# 			"base_tax_amount_after_discount_amount": tax.get("base_tax_amount_after_discount_amount"),
	# 			"item_wise_tax_detail": tax.get("item_wise_tax_detail"),
	# 		})

	sales_invoice.flags.ignore_permissions = True
	sales_invoice.run_method("set_missing_values")
	sales_invoice.save()
	sales_invoice.submit()

	return sales_invoice.name

@frappe.whitelist()
def add_to_room_bill(invoice_data):
	"""
		Validates a member using customer mapping. 
        (customer must be link to member doctypeeßßßß)
        
        Args:
            invoice_data: JSON string
				customer:  str -> Customer
				pos_profile: str -> POS Profile
				taxes_and_charges: float -> Tax And Charges
				items: array -> item list

        Returns:
            dict : A name of sales invoice
	"""
	invoice_data = json.loads(invoice_data)

	if not invoice_data.get("customer") or not invoice_data.get("items"):
		frappe.throw("Customer and Items are required.")

	member = frappe.db.get_value("Member Details" , {
		"customer"  :    invoice_data.get("customer")
	} , "name")
	if not member:
		frappe.throw("Customer is not appropriate member")
	room_reservation = frappe.db.get_value("Room Reservation" , {
		"member_id" : member
	},["name" , "sales_invoice"], as_dict = True)
	if not room_reservation:
		frappe.throw("No room reservation found for member")
	
	warehouse = None
	if invoice_data.get("pos_profile"):
		warehouse = frappe.db.get_value("POS Profile", invoice_data["pos_profile"], "warehouse")
	
	sales_invoice = frappe.get_doc("Sales Invoice" , room_reservation.sales_invoice)
	if not sales_invoice:
		frappe.throw("No invoice found for room")
	sales_invoice.update_stock = 1

	for item in invoice_data["items"]:
		sales_invoice.append("items", {
			"item_code": item["item_code"],
			"qty": item["qty"],
			"rate": item["rate"],
			"uom": item["uom"],
			"conversion_factor": item["conversion_factor"],
			"warehouse": warehouse,
		})

	if invoice_data.get("taxes_and_charges"):
		sales_invoice.taxes_and_charges = invoice_data["taxes_and_charges"]

	sales_invoice.flags.ignore_permissions = True
	sales_invoice.run_method("set_missing_values")
	sales_invoice.save()
	
	return {
		"invoice" : sales_invoice.name,
		"roomId" :  room_reservation.name
	}

# Copyright (c) 2025, Admin and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, nowdate

class MemberDetails(Document):

	@frappe.whitelist()
	def get_renewal(self):
		if not self.membership_id:
			frappe.throw("Please select a Membership ID")
		self.renewal_table = []
		doc = frappe.db.get_value("Membership", self.membership_id, ["membership_id","start_date", "end_date", "annual_fee"], as_dict=True)
		self.append("renewal_table", {
			"membership_type": doc.membership_id,
			"start_date": doc.start_date,
			"end_date": doc.end_date,
			"annual_fee": doc.annual_fee
		})
	
	def validate(self):
		if self.end_date and getdate(nowdate()) > getdate(self.end_date):
			self.is_inactive = 1
	
	def after_insert(self):
		if not frappe.db.exists("Customer", {"customer_name": self.full_name}):
			customer = frappe.get_doc({
				"doctype": "Customer",
				"customer_name": self.full_name,
				"custom_member_id": self.member_id,
				"customer_group": "Regular Members",
				"custom_email_adreess": self.email_address,
				"custom_phone_number": self.contact_number,
				"custom_date_of_birth": self.date_of_birth,
				"custom_retirement_date": self.date_of_retirement,
				"custom_expiry_date_": self.expiry_date_after_extention,
				"custom_club_no": self.club_no,
				"custom_salary_no": self.salary_code,
				"custom_fathers_name": self.father_name,
				"custom_spouses_name": self.spouse_name,
				"custom_is_member": 1,

				"custom_childs_details": [
					{
						"first_name": child.first_name,
						"last_name": child.last_name,
						"dob": child.dob
					}
					for child in self.children_details
				]
			})
			customer.insert(ignore_permissions=True)

			self.db_set("customer", customer.name)
			frappe.msgprint(f"Customer <b>{self.full_name}</b> created successfully.")

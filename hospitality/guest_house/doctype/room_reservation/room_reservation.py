# Copyright (c) 2025, Admin and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import datetime
from frappe.desk.calendar import get_event_conditions

class RoomReservation(Document):

	def validate(self):
		self.set_room_pricing_details()

	def on_submit(self):
		customer = ""

		if self.member_id:
			member = frappe.get_doc("Member Details", self.member_id)
			customer = member.customer

		elif self.guest_id:
			if self.book_against_guest:
				guest = frappe.get_doc("Guest Details", self.guest_id)
				if not guest.guest_customer:
					customer = create_customer_from_guest(guest)
					guest.db_set("guest_customer", customer)
				else:
					customer = guest.guest_customer
			else:
				if not self.guest_sponsored_by:
					frappe.throw("Sponsor member not set for guest reservation.")
				member = frappe.get_doc("Member Details", self.guest_sponsored_by)
				customer = member.customer

		if not customer:
			frappe.throw("No customer linked to this reservation.")

		si = frappe.new_doc("Sales Invoice")
		si.customer = customer
		si.due_date = frappe.utils.today()
		si.selling_price_list = "Regular Member"

		if self.sales_item and self.checkin_date and self.checkout_date:
			days = (frappe.utils.getdate(self.checkout_date) - frappe.utils.getdate(self.checkin_date)).days
			if days > 0:
				rate = get_valid_item_price(self.sales_item, "Standard Selling")
				si.append("items", {
					"item_code": self.sales_item,
					"qty": days,
					"rate": rate
				})

		for item in self.additional_purchases:
			if item.item_code and item.quantity:
				rate = get_valid_item_price(item.item_code, "Standard Selling")
				si.append("items", {
					"item_code": item.item_code,
					"qty": item.quantity,
					"rate": rate
				})

		if not si.items:
			frappe.throw("No items to bill.")

		si.insert()
		si.submit()

		frappe.msgprint(f"Sales Invoice <a href='/app/sales-invoice/{si.name}'>{si.name}</a> created for {customer}")
	
	def set_room_pricing_details(self):
		if not (self.checkin_date and self.checkout_date and self.hotel_room_price):
			return

		days = (frappe.utils.getdate(self.checkout_date) - frappe.utils.getdate(self.checkin_date)).days
		if days <= 0:
			return

		total = self.hotel_room_price * days

		formatted_rate = frappe.format_value(self.hotel_room_price, {"fieldtype": "Currency", "options": "INR"})
		formatted_total = frappe.format_value(total, {"fieldtype": "Currency", "options": "INR"})

		room_pricing_link = ""
		room_pricing = frappe.db.get_value(
			"Room Pricing",
			{
				"room_number": self.hotel_room_number,
				"rate": self.hotel_room_price
			},
			"name"
		)
		if room_pricing:
			room_pricing_link = f"<a href='/app/room-pricing/{room_pricing}' target='_blank'>{room_pricing}</a>"

		self.room_pricing_details = f"""Check-in Date		: {frappe.format_value(self.checkin_date, {'fieldtype': 'Date'})}
Check-out Date	: {frappe.format_value(self.checkout_date, {'fieldtype': 'Date'})}
Total Stay Duration	: {days} day(s)
Rate Per Day		: {formatted_rate}
Total Amount	: {formatted_total}
Room Pricing	: {room_pricing_link if room_pricing_link else "N/A"}"""

@frappe.whitelist()
def get_valid_item_price(item_code, price_list):
	today_date = frappe.utils.today()

	item_price = frappe.db.sql("""
		SELECT price_list_rate
		FROM `tabItem Price`
		WHERE item_code = %s
		AND price_list = %s
		AND (valid_upto IS NULL OR valid_upto >= %s)
		ORDER BY 
			CASE WHEN valid_upto IS NULL THEN 1 ELSE 0 END,
			valid_upto ASC
		LIMIT 1
	""", (item_code, price_list, today_date), as_dict=1)

	if item_price:
		return item_price[0].price_list_rate

	return 0

def create_customer_from_guest(guest):

	customer = frappe.get_doc({
		"doctype": "Customer",
		"customer_name": guest.full_name,
		"custom_email_adreess": guest.email_address,
		"custom_phone_number": guest.contact_number,
		"custom_date_of_birth": guest.date_of_birth,
		"custom_is_member": 0,

		"custom_childs_details": [
			{
				"first_name": child.first_name,
				"last_name": child.last_name,
				"dob": child.dob,
				"relation": child.relation
			}
			for child in guest.family_member_details
		]
	})
	customer.insert(ignore_permissions=True)
	return customer.name

@frappe.whitelist()
def get_events(start, end, filters=None):
	if isinstance(filters, str):
		filters = frappe.parse_json(filters)

	room_number = ""
	if filters and isinstance(filters, list):
		for f in filters:
			if f[1] == "hotel_room_number":
				room_number = f[3]
				break

	conditions = get_event_conditions("Room Reservation", filters)
	if conditions:
		conditions = conditions.replace("`tabRoom Reservation`.", "rr.")

	booked_reservations = frappe.db.sql(f"""
		SELECT
			rr.name,
			rr.hotel_room_number,
			rr.checkin_date,
			rr.checkout_date,
			hr.color
		FROM `tabRoom Reservation` rr
		LEFT JOIN `tabHotel Room` hr ON rr.hotel_room_number = hr.name
		WHERE (
			rr.checkin_date BETWEEN %(start)s AND %(end)s OR
			rr.checkout_date BETWEEN %(start)s AND %(end)s
		)
		AND rr.docstatus < 2
		{conditions}
	""", {
		"start": start,
		"end": end
	}, as_dict=True)


	events = []

	for res in booked_reservations:
		events.append({
			"name": res.name,
			"hotel_room_number": res.hotel_room_number or res.name,
			"checkin_date": str(res.checkin_date),
			"checkout_date": str(res.checkout_date),
			"color": "#ff4d4d" if room_number else (res.color or "#BFE2FD")
		})

	if room_number:
		booked_date_set = set()
		for res in booked_reservations:
			current = res.checkin_date
			while current <= res.checkout_date:
				booked_date_set.add(current)
				current += datetime.timedelta(days=1)

		start_date = frappe.utils.getdate(start)
		end_date = frappe.utils.getdate(end)

		current = start_date
		while current <= end_date:
			if current not in booked_date_set:
				events.append({
					"name": "",
					"hotel_room_number": "",
					"checkin_date": str(current),
					"checkout_date": str(current),
					"color": "#c6f6d5"
				})
			current += datetime.timedelta(days=1)

	return events

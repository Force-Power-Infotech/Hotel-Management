# Copyright (c) 2025, Admin and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Membership(Document):
	def validate(self):
		self.validate_dates()
		self.set_status()
		self.update_membership_item_price()

	def validate_dates(self):
		if self.start_date and self.end_date and self.end_date < self.start_date:
			frappe.throw("End date cannot be before start date.")

	def set_status(self):
		from frappe.utils import getdate, nowdate
		if self.end_date and getdate(nowdate()) > getdate(self.end_date):
			self.status = "Expired"

	def update_membership_item_price(self):
		if self.membership_type_item and self.annual_fee:
			if frappe.db.exists("Item Price", {
				"item_code": self.membership_type_item,
				"price_list": "Standard Selling"
			}):
				ip = frappe.get_doc("Item Price", {
					"item_code": self.membership_type_item,
					"price_list": "Standard Selling"
				})
				ip.price_list_rate = self.annual_fee
				ip.valid_from = self.start_date
				ip.valid_upto = self.end_date
				ip.save()
			else:
				ip = frappe.new_doc("Item Price")
				ip.item_code = self.membership_type_item
				ip.price_list = "Standard Selling"
				ip.price_list_rate = self.annual_fee
				ip.valid_from = self.start_date
				ip.valid_upto = self.end_date
				ip.save()

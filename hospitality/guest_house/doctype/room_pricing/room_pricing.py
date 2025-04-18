# Copyright (c) 2025, Admin and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RoomPricing(Document):
	def validate(self):
		self.update_pricing()

	def update_pricing(self):
		if frappe.db.exists("Item Price", {"item_code": self.sales_item}):
			ip = frappe.get_doc("Item Price", {"item_code": self.sales_item, "price_list": "Standard Selling"})
			ip.price_list_rate = self.rate
			ip.valid_from = self.from_date
			ip.valid_upto = self.to_date
			ip.save()
		else:
			ip = frappe.new_doc("Item Price")
			ip.item_code = self.sales_item
			ip.price_list = "Standard Selling"
			ip.price_list_rate = self.rate
			ip.valid_from = self.from_date
			ip.valid_upto = self.to_date
			ip.save()
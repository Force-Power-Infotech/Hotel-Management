# Copyright (c) 2025, Admin and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RoomPricing(Document):
	def after_insert(self):
		self.update_pricing()

	def update_pricing(self):
		ip = frappe.new_doc("Item Price")
		ip.item_code = self.sales_item
		ip.price_list = "Standard Selling"
		ip.price_list_rate = self.rate
		ip.valid_from = self.from_date
		ip.valid_upto = self.to_date
		ip.custom_room_pricing = self.name
		ip.insert()

		self.sales_item_price = ip.name

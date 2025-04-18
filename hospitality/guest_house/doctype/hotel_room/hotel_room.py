# Copyright (c) 2025, Admin and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class HotelRoom(Document):
	def validate(self):
		self.validate_item()


	def validate_item(self):
		if self.sales_item:
			item = frappe.get_doc("Item", self.sales_item)
			if self.is_inactive:
				item.disabled = 1
			else:
				item.disabled = 0
			item.save()

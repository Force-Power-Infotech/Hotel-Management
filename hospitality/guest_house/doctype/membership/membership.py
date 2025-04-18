# Copyright (c) 2025, Admin and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, nowdate


class Membership(Document):
	def validate(self):
		if self.start_date and self.end_date:
			if getdate(self.end_date) < getdate(self.start_date):
				frappe.throw("End Date cannot be before Start Date.")

		if self.end_date and getdate(nowdate()) > getdate(self.end_date):
			self.status = "Expired"

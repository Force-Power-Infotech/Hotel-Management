# Copyright (c) 2025, Admin and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MemberDetails(Document):

	@frappe.whitelist()
	def get_renewal(self):
		doc=frappe.get_doc("Membership", self.membership_id)
		for item in self.renewal_table:
			item.membership_type = doc.membership_type,
			item.start_date = doc.start_date,
			item.end_date = doc.end_date,



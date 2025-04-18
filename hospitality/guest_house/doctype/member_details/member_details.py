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
		doc = frappe.db.get_value("Membership", self.membership_id, ["membership_id","start_date", "end_date"], as_dict=True)
		self.append("renewal_table", {
			"membership_type": doc.membership_id,
			"start_date": doc.start_date,
			"end_date": doc.end_date,
		})

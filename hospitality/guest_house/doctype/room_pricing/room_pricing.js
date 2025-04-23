// Copyright (c) 2025, Admin and contributors
// For license information, please see license.txt

frappe.ui.form.on("Room Pricing", {
	validate(frm) {
		validate_dates(frm);
	},
});

function validate_dates(frm) {
	const from_date = frm.doc.from_date;
	const to_date = frm.doc.to_date;

	if (from_date && to_date) {
		const checkinDate = new Date(from_date);
		const checkoutDate = new Date(to_date);

		if (checkoutDate < checkinDate) {
			frappe.utils.scroll_to(frm.fields_dict.to_date.wrapper);
			frappe.throw("To Date must be after From Date.");
		}
	}
}

frappe.ui.form.on('Sales Invoice', {
	refresh: function (frm) {
		frm.add_custom_button(__('Open POS'), function () {
			const pos_url = frappe.urllib.get_full_url("/app/point-of-sale");
			window.open(pos_url, '_blank');
		});
	}
});

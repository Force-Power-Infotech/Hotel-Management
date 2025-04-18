// Copyright (c) 2025, Admin and contributors
// For license information, please see license.txt

frappe.ui.form.on('Hotel Room', {
	refresh: function(frm) {
		if (!frm.doc.__islocal) {
			frappe.call({
				method: 'frappe.client.get_list',
				args: {
					doctype: 'Member Details',
					fields: ['stay_preference'],
					filters: {
						hotel_room_type_preference: frm.doc.room_type
					},
					limit: 1000
				},
				callback: function(r) {
					const prefs = ['View', 'Smoking', 'Late Checkout'];
					const counts = {
						'View': 0,
						'Smoking': 0,
						'Late Checkout': 0
					};

					(r.message || []).forEach(row => {
						if (counts.hasOwnProperty(row.stay_preference)) {
							counts[row.stay_preference]++;
						}
					});

					let html = `
						<style>
							.preference-link {
								display: flex;
								align-items: center;
								background: #f3f3f3;
								padding: 6px 10px;
								border-radius: 6px;
								text-decoration: none;
								color: #333;
								font-size: 13px;
								font-weight: 420;
							}
							.preference-link:hover {
								text-decoration: none; /* Prevent default underline on hover */
							}
							.preference-link:hover .preference-label {
								text-decoration: underline; /* Underline only the label on hover */
							}
							.count-circle {
								background: white;
								color: #333;
								border-radius: 50%;
								width: 20px;
								height: 20px;
								display: inline-flex;
								align-items: center;
								justify-content: center;
								font-size: 12px;
								font-weight: 420;
								margin-right: 6px;
								text-decoration: none; /* Ensure count never gets underlined */
							}
						</style>
						<div style="display: flex; gap: 10px; flex-wrap: wrap;">
					`;

					prefs.forEach(pref => {
						html += `
							<a href="/app/member-details?view=list&hotel_room_type_preference=${encodeURIComponent(frm.doc.room_type)}&stay_preference=${encodeURIComponent(pref)}"
							   class="preference-link">
								<span class="count-circle">${counts[pref]}</span>
								<span class="preference-label">${pref}</span>
							</a>
						`;
					});

					html += `</div>`;
					frm.fields_dict.preference_links.$wrapper.html(html);
				}
			});
		}
	}
});

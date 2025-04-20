# Copyright (c) 2025, Admin and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import datetime
from frappe.desk.calendar import get_event_conditions

class RoomReservation(Document):
	pass

@frappe.whitelist()
def get_events(start, end, filters=None):
	if isinstance(filters, str):
		filters = frappe.parse_json(filters)

	room_number = ""
	if filters and isinstance(filters, list):
		for f in filters:
			if f[1] == "hotel_room_number":
				room_number = f[3]
				break

	conditions = get_event_conditions("Room Reservation", filters)
	if conditions:
		conditions = conditions.replace("`tabRoom Reservation`.", "rr.")

	booked_reservations = frappe.db.sql(f"""
		SELECT
			rr.name,
			rr.hotel_room_number,
			rr.checkin_date,
			rr.checkout_date,
			hr.color
		FROM `tabRoom Reservation` rr
		LEFT JOIN `tabHotel Room` hr ON rr.hotel_room_number = hr.name
		WHERE (
			rr.checkin_date BETWEEN %(start)s AND %(end)s OR
			rr.checkout_date BETWEEN %(start)s AND %(end)s
		)
		AND rr.docstatus < 2
		{conditions}
	""", {
		"start": start,
		"end": end
	}, as_dict=True)


	events = []

	for res in booked_reservations:
		events.append({
			"name": res.name,
			"hotel_room_number": res.hotel_room_number or res.name,
			"checkin_date": str(res.checkin_date),
			"checkout_date": str(res.checkout_date),
			"color": "#ff4d4d" if room_number else (res.color or "#BFE2FD")
		})

	if room_number:
		booked_date_set = set()
		for res in booked_reservations:
			current = res.checkin_date
			while current <= res.checkout_date:
				booked_date_set.add(current)
				current += datetime.timedelta(days=1)

		start_date = frappe.utils.getdate(start)
		end_date = frappe.utils.getdate(end)

		current = start_date
		while current <= end_date:
			if current not in booked_date_set:
				events.append({
					"name": "",
					"hotel_room_number": "",
					"checkin_date": str(current),
					"checkout_date": str(current),
					"color": "#c6f6d5"
				})
			current += datetime.timedelta(days=1)

	return events

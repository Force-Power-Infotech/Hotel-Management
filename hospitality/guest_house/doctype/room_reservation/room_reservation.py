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
	# Parse filters if coming as JSON string
	if isinstance(filters, str):
		filters = frappe.parse_json(filters)

	# 🔒 Ensure hotel_room_number filter is present
	room_number = ""
	if filters and isinstance(filters, list):
		for f in filters:
			if f[1] == "hotel_room_number":
				room_number = f[3]
				break
	if not room_number:
		frappe.throw("Please apply the <b>Hotel Room Number</b> filter to view calendar availability.")

	conditions = get_event_conditions("Room Reservation", filters)

	# Step 1: Get booked reservations
	booked_reservations = frappe.db.sql("""
		SELECT
			name,
			hotel_room_number,
			checkin_date,
			checkout_date
		FROM `tabRoom Reservation`
		WHERE (
			checkin_date BETWEEN %(start)s AND %(end)s OR
			checkout_date BETWEEN %(start)s AND %(end)s
		)
		AND docstatus < 2
		{conditions}
	""".format(conditions=conditions), {
		"start": start,
		"end": end
	}, as_dict=True)

	# Step 2: Build events for booked reservations (one per reservation)
	events = []

	for res in booked_reservations:
		events.append({
			"name": res.name,
			"hotel_room_number": res.name,
			"checkin_date": str(res.checkin_date),
			"checkout_date": str(res.checkout_date),
			"color": "#ff4d4d"  # red for booked
		})

	# Step 3: Add available dates as green
	# Create a set of all booked dates for quick lookup
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
				"color": "#c6f6d5"  # green for available
			})
		current += datetime.timedelta(days=1)

	return events

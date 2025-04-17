# import frappe

# def hotel_room_with_items(doc, method):
#     item_group_name = "Hotel Rooms"
#     if not frappe.db.exists("Item Group", item_group_name):
#         frappe.get_doc({
#             "doctype": "Item Group",
#             "item_group_name": item_group_name,
#             "parent_item_group": "All Item Groups",  
#             "is_group": 1  
#         }).insert(ignore_permissions=True)

#     item_name = f"Hotel Room - {doc.name}"

#     existing_item = frappe.get_all("Item", filters={"item_name": item_name}, limit=1)

#     if existing_item:
#         item_doc = frappe.get_doc("Item", existing_item[0].name)
#     else:
#         item_doc = frappe.get_doc({
#             "doctype": "Item",
#             "item_name": item_name,
#             "item_group": item_group_name,
#             "description": doc.description or f"Item for Hotel Room {doc.name}",
#             "is_stock_item": 0,  
#         })
#         item_doc.insert(ignore_permissions=True)
#     item_doc.is_disabled = 0 if doc.active == "Active" else 1
#     item_doc.save(ignore_permissions=True)
#     frappe.db.commit()



import frappe

def hotel_room_with_items(doc, method):
    # frappe.msgprint("Syncing Hotel Room with Items")
    # frappe.log_error(title="Treiggered")
    # frappe.logger().info(f"Hotel Room {doc} is being processed on save.")
    # doc=frappe.get_doc("Hotel Room", doc)
    # Ensure the item group exists
    item_group_name = "Hotel Rooms"
    
    if not frappe.db.exists("Item Group", item_group_name):
        
        frappe.get_doc({
            "doctype": "Item Group",
            "item_group_name": item_group_name,
            "parent_item_group": "All Item Groups",  # Adjust if needed
            "is_group": 1
        }).insert(ignore_permissions=True)

    # Check or create the corresponding item
    item_name = f"Hotel Room - {doc.name}"
    existing_item = frappe.get_all("Item", filters={"item_name": item_name}, limit=1)
    
    if existing_item:
        
        item_doc = frappe.get_doc("Item", existing_item[0].name)
    else:
        
        item_doc = frappe.get_doc({
            "doctype": "Item",
            "item_code": item_name,
            "item_name": item_name,
            "item_group": item_group_name,
            "description": doc.description or f"Item for Hotel Room {doc.name}",
            "is_stock_item": 0,  # Set as non-stock item
        })
        item_doc.insert(ignore_permissions=True)
    
    # Update the is_disabled field
    item_doc.disabled = 0 if doc.active == 1 else 0
    item_doc.save(ignore_permissions=True)
    frappe.db.commit()
 
def sync_member_to_customer(doc, method):
    frappe.msgprint("Syncing Member to Customer")
    """
    Sync Member Details with Customer Doctype when a Member is created or updated.
    Only update existing fields in the Customer Doctype.
    """
    # Check if a Customer exists for this Member
    customer_name = doc.full_name
    existing_customer = frappe.get_all("Customer", filters={"customer_name": customer_name}, limit=1)
    # frappe.log_error(title="Customer", message=doc.as_dict())
    # Map fields between Member Details and Customer
    mapped_fields = {
        "customer_name": doc.full_name,
        "email_id": doc.email_address,
        "mobile_no": doc.contact_number,
        "customer_type": "Individual",  # Default to Individual if not specified
        "customer_group": "Regular Members",  # Set default customer group
        "territory": "India",  # Default to India if no branch specified
        "custom_date_of_birth": doc.date_of_birth,
        "custom_club_no": doc.club_no,
        "custom_salary_n o": doc.salary_code,
        "custom_is_member":1
    }
 
    if existing_customer:
        # Update the existing Customer
        customer_doc = frappe.get_doc("Customer", existing_customer[0].name)
        for field, value in mapped_fields.items():
            if field in customer_doc.as_dict():
                customer_doc.set(field, value)
        customer_doc.save(ignore_permissions=True)
    else:
        # Create a new Customer
        customer_doc = frappe.get_doc({
            "doctype": "Customer",
            **mapped_fields,
        })
        customer_doc.save(ignore_permissions=True)
    frappe.db.commit() 

# def hotel_room_with_items(doc, method):
#     # frappe.msgprint(" membership with Items")
#     # frappe.log_error(title="Triggered")
    
#     item_group_name = "Hotel Rooms"
#     if not frappe.db.exists("Item Group", item_group_name):
#         frappe.get_doc({
#             "doctype": "Item Group",
#             "item_group_name": item_group_name,
#             "parent_item_group": "All Item Groups",  
#             "is_group": 1
#         }).insert(ignore_permissions=True)

#     item_name = f"Hotel Room - {doc}"
#     existing_item = frappe.get_all("Item", filters={"item_name": item_name}, limit=1)

#     if existing_item:
#         item_doc = frappe.get_doc("Item", existing_item[0].name)
#     else:
#         item_doc = frappe.get_doc({
#             "doctype": "Item",
#             "item_code": item_name,
#             "item_name": item_name,
#             "item_group": item_group_name,
#             # "description": doc.description or f"Item for Hotel Room {doc}",
#             "is_stock_item": 0,  
#         })
#         item_doc.insert(ignore_permissions=True)

#     item_doc.is_disabled = 0 if doc.active__inactive == "Active" else 1
#     item_doc.save(ignore_permissions=True)

#     membership_type_name = doc.membership_type 
#     if membership_type_name:
#         if frappe.db.exists("Membership Type", membership_type_name):
#             membership_doc = frappe.get_doc("Membership Type", membership_type_name)
#             membership_doc.linked_item = item_doc.name
#             membership_doc.save(ignore_permissions=True)
#             frappe.msgprint(f"Linked Item {item_doc.name} with Membership Type {membership_type_name}")
#         else:

#             frappe.log_error(f"Membership Type {membership_type_name} does not exist", title="Linking Failed")

#     frappe.db.commit()
 


def sync_guest_to_customer(doc, method):
    # doc=frappe.get_doc("Guest Details", doc)
    customer_name = doc.full_name  # Use the full name of the guest as the customer name
    customer_email = doc.email_address  # Use the guest's email for linking
    
    # Check if a customer already exists with the guest's email or name
    existing_customer = frappe.get_all(
        "Customer", 
        filters={"customer_name": customer_name}, 
        fields=["name"]
    )
    
    if existing_customer:
        # Update the existing customer
        customer_doc = frappe.get_doc("Customer", existing_customer[0].name)
        customer_doc.customer_name = doc.full_name
        customer_doc.email_id = doc.email_address
        customer_doc.mobile_no = doc.contact_number
        customer_doc.customer_group = "Individual"  # Adjust based on your configuration
        customer_doc.territory = "India"  # Adjust based on your configuration
        customer_doc.save(ignore_permissions=True)
        frappe.msgprint(f"Customer {customer_name} updated successfully.")
    else:
        # Create a new customer
        customer_doc = frappe.get_doc({
            "doctype": "Customer",
            "customer_name": doc.full_name,
            "email_id": doc.email_address,
            "mobile_no": doc.contact_number,
            "customer_group": "Individual",  # Adjust based on your configuration
            "territory": "India",  # Adjust based on your configuration
        })
        customer_doc.insert(ignore_permissions=True)
        frappe.msgprint(f"Customer {customer_name} created successfully.")

    frappe.db.commit()




def sync_room_pricing_to_item_pricing(doc, method):
    # doc=frappe.get_doc("Room Pricing", doc)
    item_code = f"Hotel Room - {doc.room}"
    price_list = "Standard Selling"  # Adjust based on your configuration
    
    # Check if the item exists in the Item doctype
    if not frappe.db.exists("Item", item_code):
        frappe.msgprint(f"Item for Room {doc.room} does not exist. Please ensure the room is linked to an item.")
        return

    # Check if item pricing already exists
    existing_price = frappe.get_all(
        "Item Price",
        filters={
            "item_code": item_code,
            "price_list": price_list,
            "valid_from": doc.from_date,
            "valid_upto": doc.to_date,  # Ensure date range matches
        },
        limit=1,
    )
    frappe.msgprint(f"Existing Price: {existing_price}")
    if existing_price:
        # Update existing item pricing
        item_price_doc = frappe.get_doc("Item Price", existing_price[0].name)
        item_price_doc.price_list_rate = doc.rate
        item_price_doc.valid_upto = doc.to_date
        item_price_doc.save(ignore_permissions=True)
        frappe.msgprint(f"Updated price for {item_code} in Item Pricing.")
    else:
        # Create new item pricing
        item_price_doc = frappe.get_doc({
            "doctype": "Item Price",
            "item_code": item_code,
            "item_name": f"Room {doc.room}",
            "item_description": f"Pricing for Hotel Room {doc.room}",
            "price_list": price_list,
            "currency": "INR",  # Adjust currency if needed
            "price_list_rate": doc.rate,
            "valid_from": doc.from_date,
            "valid_upto": doc.to_date,
            "selling": 1,  # Set as a selling price
        })
        item_price_doc.insert(ignore_permissions=True)
        frappe.msgprint(f"Created new price for {item_code} in Item Pricing.")
    
    frappe.db.commit()


def  (doc, method):
    # Fetch item matching the Hotel Room Type
    item_name = f"Hotel Room - {doc.hotel_room}"
    item = frappe.db.get_value("Item", {"item_code": item_name})

    item_data = {
        "item_code": item_name,
        "item_name": doc.room_type,
        "item_group": "Hotel Rooms",
        "stock_uom": "Nos",
        "description": f"Room Type: {doc.room_type}, Bed Type: {doc.bed_type}, Room Size: {doc.room_size}",
        "is_sales_item": 1,
        "is_purchase_item": 0,
        "include_item_in_manufacturing": 0
    }

    # Update if item exists
    if item:
        item_doc = frappe.get_doc("Item", item)
        item_doc.update(item_data)
        item_doc.save()
    else:
        # Create new item if not exists
        item_doc = frappe.get_doc({
            "doctype": "Item",
            **item_data
        })
        item_doc.insert()
    
    frappe.db.commit()

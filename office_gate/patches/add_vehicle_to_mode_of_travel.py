import frappe

def execute():
    doctype = "Travel Itinerary"
    fieldname = "mode_of_travel"

    # Desired options (first line blank)
    desired_options = ["", "Vehicle", "Flight", "Train", "Taxi"]
    options_value = "\n".join(desired_options)

    # Check if a property setter already exists
    ps = frappe.db.get_value(
        "Property Setter",
        {
            "doc_type": doctype,
            "field_name": fieldname,
            "property": "options"
        },
        ["name"],
        as_dict=True
    )

    if ps:
        # Update existing Property Setter
        frappe.db.set_value("Property Setter", ps.name, "value", options_value)
        frappe.db.commit()
    else:
        # Create new Property Setter
        frappe.get_doc({
            "doctype": "Property Setter",
            "doctype_or_field": "DocField",
            "doc_type": doctype,
            "field_name": fieldname,
            "property": "options",
            "property_type": "Text",
            "value": options_value
        }).insert(ignore_permissions=True)

    frappe.clear_cache(doctype=doctype)

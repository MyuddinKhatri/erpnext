import frappe

def execute():
	frappe.reload_doc('selling', 'doctype', 'sales_order', force=True)
	frappe.reload_doc('stock', 'doctype', 'pick_list_item', force=True)
	sales_orders = frappe.get_all("Sales Order", filters={"docstatus": 1})

	for order in sales_orders:
		pick_list_items = frappe.get_all("Pick List Item",
			filters={"docstatus": 1, "sales_order": order.name},
			fields= ["sum(qty) as total_qty", "sum(picked_qty) as picked_qty"],
			group_by="item_code")
		picked_qty = sum(d['picked_qty'] for d in pick_list_items)
		ordered_qty = sum(d['total_qty'] for d in pick_list_items)

		if picked_qty and ordered_qty:
			per_picked = (picked_qty / ordered_qty) * 100
			frappe.db.set_value("Sales Order", order.name, "per_picked", per_picked)
# -*- coding: utf-8 -*-
# Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import comma_and

class ProductRecall(Document):
	def on_submit(self):
		batch = frappe.get_doc("Batch", self.batch_no)
		items_in_warehouse = []
		items_delivered = []

		sle_list = frappe.get_list("Stock Ledger Entry", 
			[["batch_no", "=", batch.name]], ["name"])

		for sle in sle_list:
			sle_doc = frappe.get_doc("Stock Ledger Entry", sle.name).as_dict()
			sle_list.pop(0)

			if sle_doc.voucher_type == "Stock Entry":
				se = frappe.get_doc("Stock Entry", sle_doc.voucher_no).as_dict()
				for item in se.get("items"):
					if item.batch_no:
						batch_doc = frappe.get_doc("Batch", item.batch_no)
						sle_data = frappe.get_list("Stock Ledger Entry",
							[["batch_no", "=", batch_doc.name]], ["name"])
						sle_list = sle_list + sle_data
						if (item.item_code and item.batch_no and item.parent) not in items_in_warehouse:
							items_in_warehouse = items_in_warehouse + [{
								"item_code": item.item_code,
								"item_name": item.item_name,
								"batch_no": item.batch_no,
								"package_tag": item.package_tag,
								"warehouse": item.t_warehouse,
								"qty": item.qty,
								"reference_doctype": item.parenttype,
								"reference_docname": item.parent
							}]

			if sle_doc.voucher_type == "Delivery Note":
				dn = frappe.get_doc("Delivery Note", sle_doc.voucher_no).as_dict()
				for item in dn.get("items"):
					if item.batch_no:
						batch_doc = frappe.get_doc("Batch", item.batch_no)
						sle_data = frappe.get_list("Stock Ledger Entry",
							[["batch_no", "=", batch_doc.name]], ["name"])
						sle_list = sle_list + sle_data
						items_delivered = items_delivered + [{
							"customer": dn.customer,
							"item_code": item.item_code,
							"item_name": item.item_name,
							"batch_no": item.batch_no,
							"package_tag": item.package_tag,
							"qty": item.qty,
							"reference_doctype": item.parenttype,
							"reference_docname": item.parent
						}]

		items_in_warehouse = list({(v['item_code'], v['batch_no']): v for v in items_in_warehouse}.values())
		items_delivered = list({(v['item_code'], v['batch_no']): v for v in items_delivered}.values())

		prn_doc_list = []
		if items_delivered:
			doc_recall_from_customer = frappe.new_doc("Product Recall Notice")
			doc_recall_from_customer.product_recall = self.name
			doc_recall_from_customer.recall_from = "Customer"
			doc_recall_from_customer.recall_warehouse = self.recall_warehouse
			doc_recall_from_customer.update({
				"items": items_delivered
			})
			doc_recall_from_customer.save()
			prn_doc_list.append(doc_recall_from_customer)

		if items_in_warehouse:
			doc_recall_from_warehouse = frappe.new_doc("Product Recall Notice")
			doc_recall_from_warehouse.product_recall = self.name
			doc_recall_from_warehouse.recall_from = "Warehouse"
			doc_recall_from_warehouse.recall_warehouse = self.recall_warehouse
			doc_recall_from_warehouse.update({
				"items": items_in_warehouse
			})
			doc_recall_from_warehouse.save()
			prn_doc_list.append(doc_recall_from_warehouse)
		prn_doc_list = ["""<a href="#Form/Product Recall Notice/{0}">{1}</a>""".format(m.name, m.name) \
				for m in prn_doc_list]
		frappe.msgprint(_("{0} created").format(comma_and(prn_doc_list)))
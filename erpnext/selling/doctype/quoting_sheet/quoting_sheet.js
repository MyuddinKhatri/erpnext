// Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
frappe.ui.form.on('Quoting Sheet', {
	refresh: function(frm) {
		if (frm.doc.docstatus == 1){
			frm.add_custom_button(__("Update Cost"), function() {})
		}
		
	},
	item_code: function(frm) {
		if(frm.doc.currency == frappe.sys_defaults.currency){
			frm.set_value("conversion_rate", 1.0)
		}
	},
	invoke_doc_function(frm, method) {
		frappe.call({
			doc: frm.doc,
			method: method,
			callback: function(r) {
				if(!r.exe) {
					frm.refresh_fields();
				}
			}
		});
	},
	calculate: function(frm) {
		frm.events.invoke_doc_function(frm, "calculate_totals");
	},
});

frappe.ui.form.on("BOM Item", {
	item_code: function(frm,cdt,cdn) {
		let row = locals[cdt][cdn];
		frappe.call({
			method: "erpnext.selling.doctype.quoting_sheet.quoting_sheet.get_item_details_quoting_sheet",
			args: {
				"item_code": row.item_code
			},
			callback: (res)=> {
				frappe.model.set_value(cdt,cdn,"rate",res.message[0].valuation_rate)
				frappe.model.set_value(cdt,cdn,"bom_no",res.message[0].default_bom)
				frappe.model.set_value(cdt,cdn,"uom",res.message[0].stock_uom)
			},
		})																																
	},

	qty: function(frm,cdt,cdn) {
		let row = locals[cdt][cdn];
		if(row.qty && row.rate) {
			let amount = row.qty * row.rate
			frappe.model.set_value(cdt,cdn,"amount", amount)
		}
	},

	amount: function(frm,cdt,cdn) {
		let cost = 0;
		frm.doc.raw_material_items.forEach(element => {
			cost += element.amount
		});
		frm.set_value("rm_cost", cost);
	},

	rate: function(frm,cdt,cdn) {
		let row = locals[cdt][cdn];
		if(row.qty && row.rate) {
			let amount = row.qty * row.rate
			frappe.model.set_value(cdt,cdn,"amount", amount)
		}
	},

	customer_provided_item: function(frm,cdt,cdn) {
		let row = locals[cdt][cdn];
		if (row.customer_provided_item){
			frappe.model.set_value(cdt, cdn, "rate", 0.0)
			frappe.model.set_value(cdt, cdn, "amount", 0.0)
		}
		else {frappe.call({
			method: "erpnext.selling.doctype.quoting_sheet.quoting_sheet.get_item_details_quoting_sheet",
			args: {
				"item_code": row.item_code
			},
			callback: (res)=> {
				frappe.model.set_value(cdt,cdn,"rate",res.message[0].valuation_rate)
				frm.trigger("qty", cdt, cdn)
			}

		})
		
	}}
});

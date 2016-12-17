# Action Name:  Update/Fix Sale Order Margin
# Base Model:   Sales Order
# Action To Do: Execute Python Code
# Click button: Add to "More" menu

sales = self.pool["sale.order"].browse(cr, uid, context["active_ids"], context=context)
for sale in sales:
    if not sale.order_line:
        continue
    msg = "<ul><li><b>Margin:</b> " + str(sale.margin) + " &#8594; "
    sale.write({"order_line": [(1, line.id, {"product_uos_qty": line.product_uom_qty}) for line in sale.order_line]})
    msg += str(sale.margin) +"</li></ul>"
    self.message_post(cr, uid, sale.id, body=msg, type='comment', subject="Update/Fix sale order margin Server Action has been ran", subtype='html')

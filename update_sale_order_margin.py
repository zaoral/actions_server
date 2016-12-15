# Action Name:  Update/Fix Sale Order Margin
# Base Model:   Sales Order
# Action To Do: Execute Python Code
# Click button: Add to "More" menu

sales = self.pool["sale.order"].browse(cr, uid, context["active_ids"], context=context)
for sale in sales:
    old_value = sale.margin
    if not sale.order_line:
        continue
    
    sale.order_line[0].write({'purchase_price': sale.order_line[0].purchase_price * 1.0})
    new_value = sale.margin

    # Prepare log message
    if old_value == new_value:
        continue
    msg = "<ul><li><b>Margin:</b> %(old)s &#8594; %(new)s </li></ul>" % dict(old=old_value, new=sale.margin)
    self.message_post(cr, uid, sale.id, body=msg, type='comment', subject="Update/Fix sale order margin Server Action has been ran", subtype='html')

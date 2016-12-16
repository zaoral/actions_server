# Name:         Fix sale orders imported via CSV: Update UoS Qty needed for compute sale order margin
# Base Mode:    Sales Order 
# Action To Do: # Execute Python Code
# Click button: Add in the 'More' menu

# IMPORTANT: This should be run only one time to fix the error in the import
# for sale order data using csv file.

# Search messages posted when we fix the sale order margin
msg_obj = self.pool["mail.message"]
subject = "Update/Fix sale order margin Server Action has been ran"
messages = msg_obj.browse(cr, 1, msg_obj.search(cr, 1, [("subject", "ilike", subject), ("model", "=", "sale.order")]))

# Get the sale order browseables related to the posted messages.
sale_obj = self.pool["sale.order"]
sales = sale_obj.browse(cr, 1, [msg.res_id for msg in messages])

# TODO delete next lines
# raise Warning(str(len(sales)) + " " + str(sales))
sales = self.pool["sale.order"].browse(cr, uid, context["active_ids"], context=context)

for sale in sales:

    if not sale.order_line:
        continue

    msg = ""
    for line in sale.order_line:
        if line.product_uos_qty:
            continue
        msg += "<li><b>Line " + str(line.sequence2) + " - UoS Qty:</b> %s &#8594; " % line.product_uos_qty
        line.write({"product_uos_qty": line.product_uom_qty})
        msg += str(line.product_uos_qty) + "</li>"

    if not msg:
        continue

    # Trigger the changes in one of the lines to update the sale order
    # margin again to the correct value of the new lines
    msg_init = "<li><b>Margin:</b> " + str(sale.margin) + " &#8594; "
    sale.order_line[0].write({'purchase_price': sale.order_line[0].purchase_price * 1.0})
    msg_init+= str(sale.margin) + "</li>"

    self.message_post(
        cr, uid, sale.id, type='comment', subtype='html',
        body="<ul>"+msg_init+msg+"</ul>",
        subject="Fix CSV imported sale orders (UoS Qty = UoM Qty) to properly compute sale order margin")

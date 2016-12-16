# TODO delete next line
start_at = datetime.datetime.now()

# Name:         Fix sale orders imported via CSV: Update UoS Qty needed for compute sale order margin
# Base Mode:    Sales Order 
# Action To Do: # Execute Python Code
# Click button: Add in the 'More' menu

# IMPORTANT: This should be run only one time to fix the error in the import
# for sale order data using csv file.

# Search messages posted when we fix the sale order margin
msg_obj = self.pool["mail.message"]
subject = "Update/Fix sale order margin Server Action has been ran"
messages = msg_obj.browse(cr, 1, msg_obj.search(cr, 1, [("subject", "=", subject), ("model", "=", "sale.order")]))

# TODO uncomment
# # Get the sale order browseables related to the posted messages.
# sale_obj = self.pool["sale.order"]
# sales = sale_obj.browse(cr, 1, [msg.res_id for msg in messages])

# TODO delete next line
sales = self.pool["sale.order"].browse(cr, uid, context["active_ids"], context=context)

for sale in sales:
    lines2update = [line for line in sale.order_line if not line.product_uos_qty]
    if not lines2update:
        continue
    msg_margin = "<li><b>Margin:</b> " + str(sale.margin) + " &#8594; "

    sale.write({"order_line": [
        (1, line.id, {"product_uos_qty": line.product_uom_qty}) for line in lines2update]})

    msg_line_data = ''.join([
        "\n<li><b>Line " + str(line.sequence2) +
        " - UoS Qty:</b> 0.0 &#8594; " +
        str(line.product_uos_qty) + "</li>"
        for line in lines2update])
    msg_margin += str(sale.margin) + "</li>"
    self.message_post(
        cr, uid, sale.id, type='comment', subtype='html',
        body="<ul>"+msg_margin+msg_line_data+"</ul>",
        subject="Fix CSV imported sale orders (UoS Qty = UoM Qty) to properly compute sale order margin")

# Testing times
stop_at = datetime.datetime.now()
raise Warning(
    "\n Messages: " + str(len(messages)) +
    "\n New message: " + sale.message_ids[0].body +
    "\n quick enough?" "\n start at " + str(start_at) +
    "\n stop at " + str(stop_at) +
    "\n Time spent " + str(stop_at - start_at))

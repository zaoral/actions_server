# Name:         Step 1: Fix UoS qty and margin for CSV imported sale order lines
# Base Mode:    Sales Order 
# Action To Do: # Execute Python Code
# Click button: Add in the 'More' menu

# IMPORTANT: This should be run only one time to fix the error in the import
# for sale order data using csv file.

########################################################
# Using SQL

cr.execute("UPDATE sale_order_line SET product_uos_qty = product_uom_qty,  margin = (price_unit - purchase_price) * product_uom_qty")
cr.execute("""UPDATE sale_order SET margin = (
    SELECT sum(margin)
    FROM sale_order_line
    WHERE sale_order_line.order_id = sale_order.id)
""")

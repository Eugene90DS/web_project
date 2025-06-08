
import psycopg2
from app.config import DB_CONFIG

def get_contacts_and_address(order_id, company_id, route_id):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    query = '''
        SELECT c.contact_name, c.phone_number, c.priority, r.destination_address
        FROM employee_contacts c
        JOIN orders o ON o.order_id = %s
        JOIN routes r ON r.route_id = %s
        WHERE o.company_id = %s
        ORDER BY c.priority DESC
        LIMIT 3;
    '''
    cur.execute(query, (order_id, route_id, company_id))
    result = cur.fetchall()
    cur.close()
    conn.close()
    contacts = [{"name": row[0], "phone": row[1], "priority": row[2]} for row in result]
    address = result[0][3] if result else None
    return contacts, address

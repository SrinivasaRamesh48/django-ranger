
## Authentication
Most endpoints require authentication. Use the authentication endpoints to obtain the necessary credentials.

---

## **Authentication & User Management**

### Login
```http
POST /login/
```
Authenticate user and create session.

### Register
```http
POST /register/
```
Register a new user account.

### Authenticate
```http
POST /authenticate/
```
Validate user credentials.

### Logout
```http
POST /logout/
```
Terminate user session.

### Reset Password
```http
POST /reset_my_password
```
Reset user password.

### Get Active Ticket (Legacy)
```http
GET /active_ticket
```
**Note:** This is a fake endpoint for backward compatibility.

---

## **Subscribers Management**

### List All Subscribers
```http
GET /allSubscribers
```
Retrieve a list of all subscribers in the system.

---

## **ACP (Affordable Connectivity Program)**

### List ACP Enrollments
```http
GET /allACP
```
Get all ACP program enrollments.

### Enroll in ACP
```http
POST /acp_enroll
```
Enroll a subscriber in the ACP program.

### Cancel ACP Enrollment
```http
PUT /cancel_acp_enrollment/{pk}
```
Cancel an existing ACP enrollment.
- `pk`: ACP enrollment ID

---

## **Alerts Management**

### Alerts
```http
GET /alerts          # List all alerts
POST /alerts         # Create new alert
```

### Alert Details
```http
GET /alerts/{alert_id}     # Get specific alert
PUT /alerts/{alert_id}     # Update alert
PATCH /alerts/{alert_id}   # Partial update
DELETE /alerts/{alert_id}  # Delete alert
```
- `alert_id`: Unique alert identifier

### Alert Types
```http
GET /alert_types
```
Get available alert types.

### Circuit Alerts
```http
POST /circuit_alerts                    # Create circuit alert
PUT /circuit_alerts/{circuit_alert_id}  # Update circuit alert
```
- `circuit_alert_id`: Circuit alert identifier

### Home Alerts
```http
POST /home_alerts                    # Create home alert
PUT /home_alerts/{home_alert_id}     # Update home alert
```
- `home_alert_id`: Home alert identifier

### Subscriber Alerts
```http
POST /subscriber_alerts                        # Create subscriber alert
PUT /subscriber_alerts/{subscriber_alert_id}   # Update subscriber alert
```
- `subscriber_alert_id`: Subscriber alert identifier

---

## **Circuits Management**

### Circuit Carriers
```http
GET /circuit_carriers
```
List all available circuit carriers.

### Builders
```http
GET /builders
```
List all builders in the system.

### Circuits
```http
GET /allCircuits/     # List all circuits
GET /circuits_full/   # Get full circuit data
POST /circuits/       # Create new circuit
GET /circuits/{pk}/   # Get specific circuit
PUT /circuits/{pk}/   # Update circuit
```
- `pk`: Circuit ID

### Upload Circuit File
```http
POST /upload_circuit_file/{pk}/
```
Upload a file for a specific circuit.
- `pk`: Circuit ID

---

## **Billing & Payments**

### Successful Transaction Webhook
```http
POST /successful_transaction_webhook/
```
Handle successful payment transaction webhooks.

### Autopay
```http
GET /allAutopay
```
List all autopay configurations.

---

## **Interest Forms**

### Interest Form Logs
```http
GET /interest_form_logs                           # List logs
PUT /interest_form_logs/{interest_form_log_id}    # Update log
```
- `interest_form_log_id`: Interest form log identifier

---

## **Equipment Management**

### Node Classes
```http
GET /node_classes
```
List all node classes.

### Equipment
```http
GET /allEquipment        # List all equipment
POST /equipment          # Create equipment
GET /equipment/{node_id} # Get equipment details
PUT /equipment/{node_id} # Update equipment
```
- `node_id`: Equipment node identifier

### Node Frames
```http
GET /node_frames
```
List all node frames.

### Node Types
```http
GET /node_types
```
List all node types.

---

## **Networking & ONT Management**

### ONT Data
```http
GET /allONTData
```
List all ONT (Optical Network Terminal) data.

### ONT Manufacturers
```http
GET /ont_manufacturers
```
List all ONT manufacturers.

### Port MAC Address Data
```http
GET /allPortMacAddressData
```
List all port MAC address data.

---

## **Subscription Management**

### Subscription Types
```http
GET /subscription_types
```
List all available subscription types.

---

## **User Management**

### User Companies
```http
GET /user_companies
```
List all user companies.

### User Roles
```http
GET /user_roles
```
List all user roles.

### Permission Types
```http
GET /permission-types/
```
List all permission types in the system.

### Technicians
```http
GET /technicians/                              # List technicians
GET /technicians/{pk}/                         # Get technician details
PUT /technicians/{pk}/                         # Update technician
POST /technicians/{pk}/reset_password/         # Reset password
POST /technicians/{pk}/update_permissions/     # Update permissions
```
- `pk`: Technician ID

---

## **Bulk Messaging**

### Message Nodes
```http
GET /bulk_message_email_checkbox_nodes/    # Get email checkbox nodes
GET /bulk_message_phone_checkbox_nodes/    # Get phone checkbox nodes
```

### Send Messages
```http
POST /bulk_message_send_emails/    # Send bulk emails
POST /bulk_message_send_sms/       # Send bulk SMS
```

### Message Logs
```http
GET /bulk_message_subscriber_email_log/{id}/    # Get email log
GET /bulk_message_subscriber_sms_log/{id}/      # Get SMS log
```
- `id`: Log entry identifier

### Message Types
```http
GET /bulk_message_types/
```
List all bulk message types.

---

## **Message Templates**

### Email Templates
```http
POST /bulk_message_new_email_template/      # Create email template
PUT /bulk_message_edit_email_template/      # Edit email template
DELETE /bulk_message_remove_email_template/{id}/  # Remove email template
GET /bulk_message_email_template/{id}/      # Get email template
```

### Phone Templates
```http
POST /bulk_message_new_phone_template/      # Create phone template
PUT /bulk_message_edit_phone_template/      # Edit phone template
DELETE /bulk_message_remove_phone_template/{id}/  # Remove phone template
GET /bulk_message_phone_template/{id}/      # Get phone template
```
- `id`: Template identifier

---

## **Tickets Management**

### Tickets (Router-based)
```http
GET /allTickets/    # List all tickets (uses Django REST router)
```

### Ticket Operations
```http
POST /create_ticket/              # Create new ticket
POST /update_ticket/              # Update existing ticket
POST /create_ticket_entry/        # Add entry to ticket
POST /delete_ticket_entry/        # Remove entry from ticket
GET /active_ticket/               # Get currently active ticket
```

### Ticket Analytics
```http
GET /tickets_chart_data/{filter}/{timeframe}/
```
Get ticket data for charts and analytics.
- `filter`: Data filter type
- `timeframe`: Time period for data

---

## **File Management**

### Download File
```http
GET /download_file/{file_id}
```
Download a file by its ID.
- `file_id`: File identifier

---

## **Utilities**

### US States
```http
GET /us_states
```
List all US states.

---
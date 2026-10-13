# Appendix — Chift OpenAPI extract for the case endpoints

Source: openapi.json bundled in Chift's official Python SDK (PyPI package `chift`, v0.6.16), title 'Chift API'. Generated mechanically; '*' = required. Verify against docs.chift.eu before presenting.

```text

====================================================================================================
## POST /consumers/{consumer_id}/accounting/clients
summary: Create client
operationId: accounting_create_client
description: Create a new client
  param[path] consumer_id *: string(uuid) // 
  param[query] folder_id: string | null // Id of the accounting folder instance. A folder represents a legal entity within the system. Required when the multiple folders feature is enabled.
  param[query] force_merge: string | null // Indicate the ID of the corresponding supplier in the accounting system. Accounting systems using 1 entity to handle clients/customers and suppliers will merge the existing supplier with the new client/customer (if the parameter is filled in with the ID of an existing supplier).
REQUEST BODY: ClientItemIn | required

#### schema ClientItemIn
  - external_reference: string | null  // External identifier used to link the client in the accounting system with the corresponding client reference in your own system.
  - first_name: string | null  // Only used when the client is an individual (is_company=false). Indicates the first name of the client.
  - last_name: string | null  // Only used when the client is an individual (is_company=false). Indicates the last name of the client.
  - name *: string  // Full name or legal name of the client (individual or company). This is the name that will be displayed in the accounting software.
  - function: string | null  // Only used when the client is an individual (is_company=false). Indicates the function of the client.
  - is_company: boolean | null default=true  // Indicates if the client is an individual or a company.
  - company_id: string | null  // Only used when the client is an individual (is_company=false). Indicates the id of the company linked to the client.
  - phone: string | null  // Phone number of the client.
  - mobile: string | null  // Mobile phone number of the client.
  - email: string | null  // Email address of the client.
  - language: string | null  // Language of the client. Format: ISO 639-1 codes.
  - internal_notes: string | null  // Internal notes about the client.
  - website: string | null  // Website of the client.
  - vat: string | null  // VAT number of the client, used for tax compliance and invoicing. This value is unique per company and can be used as a reliable identifier to match clients between systems.
  - company_number: string | null  // National identification number of the company.
  - iban: string | null  // IBAN account number of the client.
  - bank_account: string | null  // Bank account number of the client.
  - currency: string | null  // Indicates the currency of the client (e.g., EUR).
  - active: boolean | null default=true  // Indicates if the client is active.
  - addresses *: array[AddressItemIn]  // List of addresses associated with the client.
  - account_number: string | null  // Number of ledger account assigned to the client in the accounting system as it will appear in the official accounting export file (FEC, SIE, iXBRL, etc.). This is typically the ledger account used for posting receivables. In some systems, each customer has a dedicated account; in others, a shared control account is used and customer balances are tracked in a subledger.

#### schema AddressItemIn
  - address_type *: AddressType  // 
  - name: string | null  // 
  - number: string | null  // 
  - box: string | null  // 
  - phone: string | null  // 
  - mobile: string | null  // 
  - email: string | null  // 
  - street *: string  // 
  - city *: string  // 
  - postal_code *: string  // 
  - country *: string  // Format: ISO 3166-1 codes.

#### schema AddressType
  enum ['main', 'delivery', 'invoice']
RESPONSE 200: Successful Response -> ClientItemOut

#### schema ClientItemOut
  - external_reference: string | null  // External identifier used to link the client in the accounting system with the corresponding client reference in your own system.
  - first_name: string | null  // Only used when the client is an individual (is_company=false). Indicates the first name of the client.
  - last_name: string | null  // Only used when the client is an individual (is_company=false). Indicates the last name of the client.
  - name: string | null  // Full name or legal name of the client (individual or company). This is the name displayed in the accounting software.
  - function: string | null  // Only used when the client is an individual (is_company=false). Indicates the function of the client.
  - is_company: boolean | null default=true  // Indicates if the client is an individual or a company.
  - company_id: string | null  // Only used when the client is an individual (is_company=false). Indicates the id of the company linked to the client.
  - phone: string | null  // Phone number of the client.
  - mobile: string | null  // Mobile phone number of the client.
  - email: string | null  // Email address of the client.
  - language: string | null  // Language of the client. Format: ISO 639-1 codes.
  - internal_notes: string | null  // Internal notes about the client.
  - website: string | null  // Website of the client.
  - vat: string | null  // VAT number of the client.
  - company_number: string | null  // National identification number of the company.
  - iban: string | null  // IBAN account number of the client. DEPRECATED see bank_accounts
  - bank_account: string | null  // Bank account number of the client. DEPRECATED see bank_accounts
  - currency: string | null  // Indicates the currency of the client (e.g., EUR).
  - active: boolean | null default=true  // Indicates if the client is active.
  - account_number: string | null  // Ledger account number assigned to the customer in the accounting system as it will appear in the official accounting export file (FEC, SIE, iXBRL, etc.).
  - id: string | null  // Id of the client in the accounting software. This is the unique identifier used to reference the client in the system.
  - last_updated_on: string(date-time) | null  // The last time the client has been updated.
  - addresses: array[AddressItemOut] | null default=[]  // List of addresses associated with the client.
  - third_party_account: string | null  // Third party account number/code representing the client in the accounting software.
  - bank_accounts: array[BankAccountsItem] | null  // List of bank accounts information associated with the client.

#### schema AddressItemOut
  - address_type *: AddressType  // 
  - name: string | null  // 
  - number: string | null  // 
  - box: string | null  // 
  - phone: string | null  // 
  - mobile: string | null  // 
  - email: string | null  // 
  - street: string | null  // 
  - city: string | null  // 
  - postal_code: string | null  // 
  - country: string | null  // Format: ISO 3166-1 codes.

#### schema BankAccountsItem
  - is_primary: boolean | null default=true  // Indicates whether this is the default bank account for this third-party. Only one bank account per third-party can have is_primary set to true. Defaults to true.
  - currency: string | null  // Indicates the currency of the bank account (e.g., EUR).
  - iban: string | null  // International Bank Account Number (ISO 13616). Present for countries in the IBAN scheme (e.g., France, Germany, United Kingdom). null for countries that do not participate in the IBAN scheme (e.g., US, Canada, Australia).
  - bic_swift: string | null  // Bank Identifier Code (ISO 9362), also known as SWIFT code. 8 or 11 characters. Optional for domestic payments, but required for international wire transfers.
  - account_number: string | null  // Local bank account number. Used when the country does not participate in the IBAN scheme (e.g., US, CA, AU). Always paired with a routing_code.
  - routing_code: RoutingCodeItem | null  // Domestic routing identifier for the bank. Required when no iban is present. Contains two subfields: type and value

#### schema RoutingCodeItem
  - type: BankAccountRoutingType default="unknown"  // The routing format. Possible values: ach (US), sort_code (UK), bsb (AU), transit (CA), ifsc (IN), clabe (MX).
  - value: string | null  // The raw routing code value, without spaces or dashes.

#### schema BankAccountRoutingType
  enum ['unknown', 'ach', 'sort_code', 'bsb', 'transit', 'ifsc', 'clabe']
RESPONSE 400: Bad Request -> ChiftError
RESPONSE 422: Unprocessable Entity -> ChiftError

====================================================================================================
## POST /consumers/{consumer_id}/accounting/invoices/multi-analytic-plans
summary: Create sale/purchase entry (Multiple plans)
operationId: accounting_create_invoice_multiple_plans
description: Create a new sale/purchase entry with multiple analytic plans in the accounting
  param[path] consumer_id *: string(uuid) // 
  param[query] folder_id: string | null // Id of the accounting folder instance. A folder represents a legal entity within the system. Required when the multiple folders feature is enabled.
  param[query] force_financial_period: string | null // Forces financial period in which the invoice must be created. This will create the invoice in the forced financial period rather than the current period. The format is: mmYYYY.
  param[query] regroup_lines: BoolParam | null default="true" // Regroup lines by account number, tax code and analytic distribution in the accounting system.
  param[query] ignore_accounting_id: boolean default=false // If set to true, Chift will not wait for the invoice to be processed to return, use this when you do not need the ID in the return value.Note that this might also change the output of the call.
  param[query] force_currency_exchange: boolean | null default=false // Boolean flag indicating whether to force the use of the provided currency exchange rate instead of the rate used by the accounting software. 
REQUEST BODY: InvoiceItemInMultiAnalyticPlans | required

#### schema InvoiceItemInMultiAnalyticPlans
  - invoice_type *: InvoiceType  // Specifies the type of invoice
  - invoice_number: string | null  // Unique 'number' of the invoice instance in the accounting software. This is an internal reference number. if not specified, will be automatically generated according to the system’s numbering rules. It does not necessarily match the number displayed on an invoice.It is recommended to use this number for idempotency to prevent duplicate entries. Refer to the idempotency documentation in the Developer Guides for more details
  - currency *: string  // Code (e.g., USD, EUR) of the currency used for invoice amounts.
  - untaxed_amount *: number  // Total amount of the invoice excluding taxes.
  - tax_amount *: number  // Total amount of tax applied to the invoice
  - total *: number  // Total amount of the invoice, including taxes (untaxed_amount + tax_amount).
  - reference: string | null  // Optional reference field used to store an external or contextual identifier related to the entry. For purchase invoices, it typically contains the invoice number issued by the supplier. For sales invoices, it may reference a quote number or any other relevant document. Unlike number, this field is not subject to specific format or character restrictions and can hold free-form text.
  - payment_communication: string | null  // Field containing the payment reference or communication associated with the invoice (e.g., bank transfer reference, SEPA remittance message). Often used for reconciliation purposes.
  - customer_memo: string | null  // Internal or external note associated with the invoice, typically intended for the customer. Can include additional context, comments, or special instructions related to the transaction.
  - payment_term_id: string | null  // Technical ID of the payment term associated with the invoice.
  - withholding_tax: WithholdingTax | null  // Withholding tax information for the invoice.
  - invoice_date *: string(date)  // Accounting date of the invoice (format: YYYY-MM-DD).
  - due_date *: string(date)  // Due date for payment or settlement (format: YYYY-MM-DD).
  - partner_id: string | null  // Id of the related third party (supplier or customer) in the accounting software. Used to link the invoice to the corresponding client or supplier record in the accounting system.
  - journal_id: string | null  // Identifier of the journal for the invoice. If not provided, the journal will be set automatically if only one exists; otherwise, an error will be thrown.
  - status: InvoiceStatusIn | null default="posted"  // string indicating if invoice has been posted (finalized) in the accounting system.
  - pdf: string | null  // Base 64 string representing the PDF attached to the invoice.
  - pdf_name: string | null  // A name for the PDF file to be created for accounting software that support it.
  - currency_exchange_rate: number | null default=1  // Exchange rate applicable at the date of the invoice. Required when the invoice currency is different from the folder's default currency.
  - invoice_correction: InvoiceCorrection | null  // Information used to add a correction line when roundings have an impact on the total amount of the invoice.
  - nl_payment_terms_split: NlPaymentTermsSplit | null  // NL only - For Dutch split payment compliance (G/N-rekening): use to specify how invoice amounts are divided between a blocked (G) and normal (N) account in high-risk sectors (e.g., construction, staffing).
  - shipping_country: string | null  // Format: ISO 3166-1 codes.
  - partner_info: AccountToCreate | null  // Information about the client/supplier that must be created. In some tools we cannot create a client/supplier by API. Missing clients/suppliers must be explicitly provided during the invoice creation and will be automatically created by the accounting software. This is for example the case for Tiime.
  - lines *: array[InvoiceLineItemInMultiAnalyticPlans]  // 
  - start_date: string(date) | null  // Start date of the period covered by the invoice (format: YYYY-MM-DD). This field should be used when the invoice relates to prepaid income or expenses (accruals and deferrals), indicating when the covered period begins.
  - end_date: string(date) | null  // End date of the period covered by the invoice (format: YYYY-MM-DD). This field should be used when the invoice relates to prepaid income or expenses (accruals and deferrals), indicating when the covered period ends.
  - payment_method_id: string | null  // Technical ID of the payment method in the accounting system. This is an indication of the payment method that will be used to pay the invoice. It is not necessarily the payment method that will eventually be used to pay the invoice.
  - delivery_date: string(date) | null  // Date on which the goods were delivered or the service was provided (format: YYYY-MM-DD). Used to assign the invoice and its tax to the correct period when it differs from the invoice date.

#### schema InvoiceType
  enum ['customer_invoice', 'customer_refund', 'supplier_invoice', 'supplier_refund']

#### schema WithholdingTax
  - tax_rate *: number  // Rate of the withholding tax. Normal withholding tax should have a negative tax rate.
  - tax_code *: string  // Tax code of the withholding tax. This is the Id of the Tax Code in the accounting software.
  - tax_amount *: number  // Amount of the withholding tax. This is the amount of the withholding tax that will be applied to the invoice. It should be negative for normal withholding tax.

#### schema InvoiceStatusIn
  enum ['draft', 'posted']

#### schema InvoiceCorrection
  - sale_invoice_correction_tax_code: string | null  // Tax code to apply on the correction line when the invoice is a sale (customer invoice). Required only when invoice_correction is used for a sale invoice or refund.
  - purchase_invoice_correction_tax_code: string | null  // Tax code to apply on the correction line when the invoice is a purchase (supplier invoice). Required only when invoice_correction is used for a purchase invoice or refund.
  - invoice_correction_credit_account_number: string | null  // Account number to use for the correction line on a sale (customer invoice).
  - invoice_correction_debit_account_number: string | null  // Account number to use for the correction line on a purchase (supplier invoice).

#### schema NlPaymentTermsSplit
  - g_account *: PaymentTermAccountInfo  // This is the 'Geblokkeerde rekening' in Dutch. It is a blocked bank account used only for tax-related payments, such as VAT and payroll tax.
  - n_account *: PaymentTermAccountInfo  // This is the 'Normale rekening' in Dutch. It is a regular bank account used for standard business operations and unrestricted funds. The non-tax portion of the invoice is paid here.

#### schema PaymentTermAccountInfo
  - amount *: number  // Amount to be paid to the G or N account
  - iban *: string  // IBAN of the G or R account

#### schema AccountToCreate
  - account_number *: string  // 
  - account_name *: string  // 

#### schema InvoiceLineItemInMultiAnalyticPlans
  - line_number: integer | null default=1  // Optional line sequence number used to preserve the order of invoice items.
  - unit_price *: number  // Unit price of the item, before tax.
  - unit_of_measure: string | null  // A list of default units can be used for which an advanced mapping has been done (units: 'hour', 'day', 'cm', 'm2', 'm3', 'm', 'km', 'mile', 'g', 'kg', 'ton', 'box', 'pallet', 'roll', 'liter', 'unit'). Custom units of measure must have an identical name in the target software.
  - quantity *: number  // Quantity of items. This is the amount of units sold or purchased.
  - untaxed_amount *: number  // Amount excluding tax for the line item (i.e., unit_price × quantity).
  - tax_rate *: number  // Tax rate used for the line (e.g., 21.0).
  - tax_amount *: number  // Tax amount calculated for the line (i.e. untaxed_amount * tax_rate).
  - total *: number  // Total amount for the item, including tax (untaxed_amount + tax_amount).
  - account_number *: string  // Ledger account number (of type general) used for the line (e.g., 701000).
  - tax_code *: string  // Indicates the tax code used for the line. This is the Id of the Tax Code in the accounting software.
  - description: string default=""  // Text description for this line item.
  - analytic_distribution: array[AnalyticDistribution] | null default=[]  // 

#### schema AnalyticDistribution
  - analytic_plan *: string  // Id of the analytic plan to which the distribution applies.
  - analytic_accounts *: array[AnalyticDistributionDetail]  // List of analytic accounts and their respective percentages for the distribution.

#### schema AnalyticDistributionDetail
  - analytic_account *: string  // 
  - percentage *: number  // Percentage of the untaxed amount attributed to this analytic account. Only whole numbers (no decimals) are allowed. The total across the analytic distribution (all accounts in a given analytic plan) must equal 100%.
RESPONSE 200: Successful Response -> InvoiceItemOutMultiAnalyticPlans

#### schema InvoiceItemOutMultiAnalyticPlans
  - invoice_type *: InvoiceType  // Specifies the type of invoice
  - invoice_number: string | null  // Unique 'number' of the invoice instance in the accounting software. This is an internal reference number. if not specified, will be automatically generated according to the system’s numbering rules. It does not necessarily match the number displayed on an invoice.It is recommended to use this number for idempotency to prevent duplicate entries. Refer to the idempotency documentation in the Developer Guides for more details
  - currency *: string  // Code (e.g., USD, EUR) of the currency used for invoice amounts.
  - untaxed_amount *: number  // Total amount of the invoice excluding taxes.
  - tax_amount *: number  // Total amount of tax applied to the invoice
  - total *: number  // Total amount of the invoice, including taxes (untaxed_amount + tax_amount).
  - reference: string | null  // Optional reference field used to store an external or contextual identifier related to the entry. For purchase invoices, it typically contains the invoice number issued by the supplier. For sales invoices, it may reference a quote number or any other relevant document. Unlike number, this field is not subject to specific format or character restrictions and can hold free-form text.
  - payment_communication: string | null  // Field containing the payment reference or communication associated with the invoice (e.g., bank transfer reference, SEPA remittance message). Often used for reconciliation purposes.
  - customer_memo: string | null  // Internal or external note associated with the invoice, typically intended for the customer. Can include additional context, comments, or special instructions related to the transaction.
  - payment_term_id: string | null  // Technical ID of the payment term associated with the invoice.
  - withholding_tax: WithholdingTax | null  // Withholding tax information for the invoice.
  - id: string | null  // 
  - invoice_date *: string(date)  // Accounting invoice date. It is automatically set to '1970-01-01' if the value is empty in the accounting system.
  - due_date *: string(date)  // Last Due date of the invoice. The invoice date is used when this information is not given by the software.
  - delivery_date: string(date) | null  // Date on which the goods were delivered or the service was provided (format: YYYY-MM-DD), when the accounting system exposes it.
  - partner_id *: string | null  // 
  - journal_id: string | null  // Indicates the journal used in for the invoice. If the journal is not given, the journal will be automatically set if only one journal exists otherwise an error will be thrown.
  - payments: array[Payment] | null  // 
  - status: InvoiceStatusOut | null default="posted"  // 
  - last_updated_on: string(date-time) | null  // The last time the invoice has been updated.
  - partner: Partner | null  // Extra information about the partner (client/supplier) linked to the invoice. To ensure this information is returned, you need to use the include_partner_info query parameter.
  - due_dates: array[InvoiceItemDueDatesOut] | null default=[]  // List of all due dates of the invoice.
  - attachments_info: ItemAttachmentInfoOut  // Indicates whether a file attachment (e.g. PDF or image) is linked to this invoice and how to retrieve it. Check the status field: 'yes' means a direct download URL is available in the attachments array; 'yes_to_request' means the file exists but must be fetched separately via GET /accounting/attachments?type=invoice&document_id={id}, which returns the file as a base64-encoded string. 'no' means no attachment is linked. 'unknown' means the connector does not support this.
  - accounting_info: AccountingInfoOut | null  // Additional information about the invoice.
  - payment_method_id: string | null  // Technical ID of the payment method in the accounting system. This is the payment method currently linked to the invoice. It is not necessarily the payment method that will eventually be used to pay the invoice.
  - approval_status: InvoiceApprovalStatus default="unknown"  // Approval status of the invoice.
  - lines *: array[InvoiceLineItemOutMultiAnalyticPlans]  // 

#### schema Payment
  - id *: string  // 
  - name *: string  // 
  - currency *: string  // 
  - amount *: number  // Total amount of the payment. A part of this amount could be reconciled with another invoice.
  - dedicated_amount: number default=0  // Amount of the payment dedicated to the invoice. 
  - payment_date *: string(date)  // 
  - journal_type *: JournalType  // 
  - journal_id *: string  // 
  - journal_name *: string  // 
  - reconciled: boolean | null default=false  // 
  - communication: string | null  // 
  - matching_number: string | null  // 

#### schema JournalType
  enum ['customer_invoice', 'customer_refund', 'supplier_invoice', 'supplier_refund', 'financial_operation', 'miscellaneous_operation', 'unknown']

#### schema InvoiceStatusOut
  enum ['cancelled', 'draft', 'posted', 'paid']

#### schema Partner
  - external_reference: string | null  // External identifier used to link the client in the accounting system with the corresponding client reference in your own system.
  - first_name: string | null  // Only used when the client is an individual (is_company=false). Indicates the first name of the client.
  - last_name: string | null  // Only used when the client is an individual (is_company=false). Indicates the last name of the client.
  - name: string | null  // Full name or legal name of the client (individual or company). This is the name displayed in the accounting software.
  - function: string | null  // Only used when the client is an individual (is_company=false). Indicates the function of the client.
  - is_company: boolean | null default=true  // Indicates if the client is an individual or a company.
  - company_id: string | null  // Only used when the client is an individual (is_company=false). Indicates the id of the company linked to the client.
  - phone: string | null  // Phone number of the client.
  - mobile: string | null  // Mobile phone number of the client.
  - email: string | null  // Email address of the client.
  - language: string | null  // Language of the client. Format: ISO 639-1 codes.
  - internal_notes: string | null  // Internal notes about the client.
  - website: string | null  // Website of the client.
  - vat: string | null  // VAT number of the client.
  - company_number: string | null  // National identification number of the company.
  - iban: string | null  // IBAN account number of the client. DEPRECATED see bank_accounts
  - bank_account: string | null  // Bank account number of the client. DEPRECATED see bank_accounts
  - currency: string | null  // Indicates the currency of the client (e.g., EUR).
  - active: boolean | null default=true  // Indicates if the client is active.
  - account_number: string | null  // Ledger account number assigned to the customer in the accounting system as it will appear in the official accounting export file (FEC, SIE, iXBRL, etc.).
  - id: string | null  // Id of the client in the accounting software. This is the unique identifier used to reference the client in the system.
  - last_updated_on: string(date-time) | null  // The last time the client has been updated.
  - addresses: array[AddressItemOut] | null default=[]  // List of addresses associated with the client.
  - third_party_account: string | null  // Third party account number/code representing the client in the accounting software.
  - bank_accounts: array[BankAccountsItem] | null  // List of bank accounts information associated with the client.

#### schema AddressItemOut
  - address_type *: AddressType  // 
  - name: string | null  // 
  - number: string | null  // 
  - box: string | null  // 
  - phone: string | null  // 
  - mobile: string | null  // 
  - email: string | null  // 
  - street: string | null  // 
  - city: string | null  // 
  - postal_code: string | null  // 
  - country: string | null  // Format: ISO 3166-1 codes.

#### schema AddressType
  enum ['main', 'delivery', 'invoice']

#### schema BankAccountsItem
  - is_primary: boolean | null default=true  // Indicates whether this is the default bank account for this third-party. Only one bank account per third-party can have is_primary set to true. Defaults to true.
  - currency: string | null  // Indicates the currency of the bank account (e.g., EUR).
  - iban: string | null  // International Bank Account Number (ISO 13616). Present for countries in the IBAN scheme (e.g., France, Germany, United Kingdom). null for countries that do not participate in the IBAN scheme (e.g., US, Canada, Australia).
  - bic_swift: string | null  // Bank Identifier Code (ISO 9362), also known as SWIFT code. 8 or 11 characters. Optional for domestic payments, but required for international wire transfers.
  - account_number: string | null  // Local bank account number. Used when the country does not participate in the IBAN scheme (e.g., US, CA, AU). Always paired with a routing_code.
  - routing_code: RoutingCodeItem | null  // Domestic routing identifier for the bank. Required when no iban is present. Contains two subfields: type and value

#### schema RoutingCodeItem
  - type: BankAccountRoutingType default="unknown"  // The routing format. Possible values: ach (US), sort_code (UK), bsb (AU), transit (CA), ifsc (IN), clabe (MX).
  - value: string | null  // The raw routing code value, without spaces or dashes.

#### schema BankAccountRoutingType
  enum ['unknown', 'ach', 'sort_code', 'bsb', 'transit', 'ifsc', 'clabe']

#### schema InvoiceItemDueDatesOut
  - due_date *: string(date)  // Due date of the item.
  - payment_method: string | null  // Payment method used to pay the invoice on that due date.
  - payment_method_id: string | null  // Technical ID of the payment method used to pay the invoice on that due date.
  - amount *: number  // Amount due for the invoice on that due date. A positive amount represents debit on customer invoices and supplier refunds or credit on supplier invoices and customer refunds. A negative amount represents credit on customer invoices and supplier refunds or debit on supplier invoices and customer refunds.

#### schema ItemAttachmentInfoOut
  - status *: ItemAttachmentInfoStatus  // Indicates whether an attachment (e.g. PDF or image) is available for this entry, and how to retrieve it. 'yes': one or more attachments are available directly — each entry in the attachments array contains a filename and a download URL. 'yes_to_request': an attachment exists but cannot be returned inline. Call GET /accounting/attachments with type and document_id to retrieve the file as a base64-encoded string. The attachments array may be empty in this case. 'no': no attachment is linked to this entry. 'unknown': the connector does not support attachment detection for this provider.
  - attachments: array[ItemAttachmentInfoAttachment] | null default=[]  // List of attachments available directly for this entry. Populated only when status is 'yes'. When status is 'yes_to_request', this list is empty — use GET /accounting/attachments to fetch the file content.

#### schema ItemAttachmentInfoStatus
  enum ['unknown', 'yes', 'yes_to_request', 'no']

#### schema ItemAttachmentInfoAttachment
  - filename: string | null  // The name of the attachment.
  - url: string | null  // Direct download URL for the attachment file. Only populated when the parent attachments_info.status is 'yes'. When status is 'yes_to_request', this field is null and the file must be retrieved via GET /accounting/attachments with the appropriate type and document_id, which returns the content as a base64-encoded string.

#### schema AccountingInfoOut
  - main_currency: string  // Main currency of the accounting folder. ISO-4217 format.
  - main_currency_total: number default=0  // Total amount of the invoice in the accounting folder's currency.
  - account_number: string | null  // Client/supplier ledger account used to book the invoice total amount. (optional)

#### schema InvoiceApprovalStatus
  enum ['unknown', 'pending', 'approved', 'rejected']

#### schema InvoiceLineItemOutMultiAnalyticPlans
  - line_number: integer | null default=1  // Optional line sequence number used to preserve the order of invoice items.
  - unit_price *: number  // Unit price of the item, before tax.
  - unit_of_measure: string | null  // A list of default units can be used for which an advanced mapping has been done (units: 'hour', 'day', 'cm', 'm2', 'm3', 'm', 'km', 'mile', 'g', 'kg', 'ton', 'box', 'pallet', 'roll', 'liter', 'unit'). Custom units of measure must have an identical name in the target software.
  - quantity *: number  // Quantity of items. This is the amount of units sold or purchased.
  - untaxed_amount *: number  // Amount excluding tax for the line item (i.e., unit_price × quantity).
  - tax_rate *: number  // Tax rate used for the line (e.g., 21.0).
  - tax_amount *: number  // Tax amount calculated for the line (i.e. untaxed_amount * tax_rate).
  - total *: number  // Total amount for the item, including tax (untaxed_amount + tax_amount).
  - account_number: string | null  // Ledger account number (of type general) used for the line (e.g., 701000).
  - tax_code: string | null  // Indicates the tax code used for the line. This is the Id of the Tax Code in the accounting software.
  - description: string | null default=""  // Text description for this line.
  - analytic_distribution: array[AnalyticDistribution] | null default=[]  // List of analytic distributions for the line item. Each distribution specifies an analytic plan and the associated analytic accounts with their percentages.
RESPONSE 400: Bad Request -> ChiftError
RESPONSE 422: Unprocessable Entity -> ChiftError
RESPONSE 409: Conflict -> ChiftError
RESPONSE 404: Not Found -> ChiftError

====================================================================================================
## GET /consumers/{consumer_id}/accounting/outstandings
summary: Get clients/suppliers outstanding items
operationId: accounting_get_outstandings
description: Returns a list of all clients/suppliers outstanding items
  param[path] consumer_id *: string(uuid) // 
  param[query] page: integer default=1 // Page number
  param[query] size: integer default=50 // Page size
  param[query] folder_id: string | null // Id of the accounting folder instance. A folder represents a legal entity within the system. Required when the multiple folders feature is enabled.
  param[query] type *: OutstandingType // 
  param[query] unposted_allowed *: BoolParam // 
RESPONSE 200: Successful Response -> ChiftPage_OutstandingItem_

#### schema ChiftPage_OutstandingItem_
  - items *: array[OutstandingItem]  // 
  - total *: integer  // 
  - page *: integer  // 
  - size *: integer  // 

#### schema OutstandingItem
  - id *: string  // Unique id of the outstanding item instance in the accounting system.
  - number: string | null  // Invoice, Journal entry or Financial entry number of the outstanding item.
  - journal_id *: string  // Id of the journal instance associated with the outstanding item.
  - journal_type *: JournalType  // Type of the journal associated with the outstanding item. This indicates the type of journal in which the outstanding item is recorded, such as 'sales', 'purchases', 'bank', etc. It helps in categorizing the outstanding item based on the nature of the transaction.
  - date *: string(date)  // Accounting date of the outstanding item.
  - due_date: string(date) | null  // Due date of the outstanding item.
  - due_dates: array[OutstandingItemDueDatesOut] | null default=[]  // List of all due dates of the outstanding.
  - currency *: string  // Currency of the outstanding item (e.g., EUR, USD).
  - currency_exchange_rate *: number  // Exchange rate applicable at the date of the outstanding item if currency different from folder's default currency.
  - amount *: number  // Total amount
  - open_amount *: number  // Open amount.
  - partner_id *: string  // Id of the thirdparty (customer, supplier or employee) in the accounting system linked to the outstanding item. This is used to identify the entity associated with the outstanding item.
  - account_number *: string  // Account number in the chart of accounts associated with the outstanding item. This is typically used to book the outstanding item against a specific ledger account.
  - reference: string | null  // Reference of the outstanding item. This is an optional field that can be used to store additional information or context related to the outstanding item, such as an invoice number or a transaction reference.
  - matching_numbers: array[string] | null default=[]  // List of matching numbers associated with the outstanding item. This is used to track any matching operations that have been performed on the outstanding item, such as payments or adjustments.
  - payment_communication: string | null  // Payment communication associated with the outstanding item. This is an optional field that can be used to store additional information related to the payment
  - posted *: boolean  // Indicates if the outstanding item has been posted (finalized) in the accounting system. If not provided, it defaults to True.
  - original_document: OriginalOutstandingItem | null  // Details of the original document associated with the outstanding item. This is used to link the outstanding item to its original source when oustanding item was initially posted in previous bookyear.

#### schema JournalType
  enum ['customer_invoice', 'customer_refund', 'supplier_invoice', 'supplier_refund', 'financial_operation', 'miscellaneous_operation', 'unknown']

#### schema OutstandingItemDueDatesOut
  - due_date *: string(date)  // Due date of the outstanding item.
  - payment_method: string | null  // Payment method used to pay the outstanding on that due date.
  - payment_method_id: string | null  // Technical ID of the payment method used to pay the outstanding on that due date.
  - amount *: number  // Amount due for the outstanding on that due date.

#### schema OriginalOutstandingItem
  - id: string | null  // Unique id of the original outstanding item in the accounting system.
  - number: string | null  // Number of the original outstanding item.
  - journal_id: string | null  // Id of the journal associated with the original outstanding item.
  - journal_type: JournalType | null  // Type of the journal associated with the original outstanding item.
  - date: string(date) | null  // Date of the original outstanding item.
  - due_date: string(date) | null  // Due date of the original outstanding item.
  - reference: string | null  // Reference of the original outstanding item.
RESPONSE 400: Bad Request -> ChiftError
RESPONSE 422: Validation Error -> HTTPValidationError

====================================================================================================
## GET /consumers/{consumer_id}/accounting/invoices/multi-analytic-plans/type/{invoice_type}
summary: Get invoices by type (sale/purchase entries - Multiple Analytic Plans)
operationId: accounting_get_invoices_by_type_multi_analytic_plans
description: Returns a list of invoices by a specific type (=sale/purchase entries) with invoice lines including multiple analytic plans. Optionally dates can be defined to retrieve invoice from a certain date to another date
  param[path] consumer_id *: string(uuid) // 
  param[path] invoice_type *: InvoiceType // 
  param[query] page: integer default=1 // Page number
  param[query] size: integer default=50 // Page size
  param[query] folder_id: string | null // Id of the accounting folder instance. A folder represents a legal entity within the system. Required when the multiple folders feature is enabled.
  param[query] date_from: string(date) | null // 
  param[query] date_to: string(date) | null // 
  param[query] journal_ids: string | null // Journal Ids used to filter the invoices. The Ids are separated by ','
  param[query] include_payments: BoolParam | null default="false" // Indicate if payments linked to the invoices should be included in the response. By default payments are not included and the field payments is null.
  param[query] payment_status: PaymentStatus | null default="all" // Extra filter to retrieve invoices with a specific payment status. Cancelled invoices are filtered out when using either paid or unpaid.
  param[query] updated_after: string(date-time) | null // Retrieve invoices created or updated after a specific datetime (e.g. 2023-01-31T15:00:00 for 31 of January 2023 at 3PM UTC). UTC is the only format that is supported on all connectors.
  param[query] include_invoice_lines: BoolParam | null default="false" // Indicate if invoice lines should be included in the response. By default invoice lines are not included when this requires extra requests on the target API.
  param[query] include_partner_info: BoolParam | null default="false" // Indicate if partner (client/supplier) information should be included in the response. By default partner information is not included when it requires extra requests on the target API to be retrieved.
  param[query] approval_status: InvoiceApprovalStatusFilter | null // Filter invoices by approval status.
RESPONSE 200: Successful Response -> ChiftPage_InvoiceItemOutMultiAnalyticPlans_

#### schema ChiftPage_InvoiceItemOutMultiAnalyticPlans_
  - items *: array[InvoiceItemOutMultiAnalyticPlans]  // 
  - total *: integer  // 
  - page *: integer  // 
  - size *: integer  // 

#### schema InvoiceItemOutMultiAnalyticPlans
  - invoice_type *: InvoiceType  // Specifies the type of invoice
  - invoice_number: string | null  // Unique 'number' of the invoice instance in the accounting software. This is an internal reference number. if not specified, will be automatically generated according to the system’s numbering rules. It does not necessarily match the number displayed on an invoice.It is recommended to use this number for idempotency to prevent duplicate entries. Refer to the idempotency documentation in the Developer Guides for more details
  - currency *: string  // Code (e.g., USD, EUR) of the currency used for invoice amounts.
  - untaxed_amount *: number  // Total amount of the invoice excluding taxes.
  - tax_amount *: number  // Total amount of tax applied to the invoice
  - total *: number  // Total amount of the invoice, including taxes (untaxed_amount + tax_amount).
  - reference: string | null  // Optional reference field used to store an external or contextual identifier related to the entry. For purchase invoices, it typically contains the invoice number issued by the supplier. For sales invoices, it may reference a quote number or any other relevant document. Unlike number, this field is not subject to specific format or character restrictions and can hold free-form text.
  - payment_communication: string | null  // Field containing the payment reference or communication associated with the invoice (e.g., bank transfer reference, SEPA remittance message). Often used for reconciliation purposes.
  - customer_memo: string | null  // Internal or external note associated with the invoice, typically intended for the customer. Can include additional context, comments, or special instructions related to the transaction.
  - payment_term_id: string | null  // Technical ID of the payment term associated with the invoice.
  - withholding_tax: WithholdingTax | null  // Withholding tax information for the invoice.
  - id: string | null  // 
  - invoice_date *: string(date)  // Accounting invoice date. It is automatically set to '1970-01-01' if the value is empty in the accounting system.
  - due_date *: string(date)  // Last Due date of the invoice. The invoice date is used when this information is not given by the software.
  - delivery_date: string(date) | null  // Date on which the goods were delivered or the service was provided (format: YYYY-MM-DD), when the accounting system exposes it.
  - partner_id *: string | null  // 
  - journal_id: string | null  // Indicates the journal used in for the invoice. If the journal is not given, the journal will be automatically set if only one journal exists otherwise an error will be thrown.
  - payments: array[Payment] | null  // 
  - status: InvoiceStatusOut | null default="posted"  // 
  - last_updated_on: string(date-time) | null  // The last time the invoice has been updated.
  - partner: Partner | null  // Extra information about the partner (client/supplier) linked to the invoice. To ensure this information is returned, you need to use the include_partner_info query parameter.
  - due_dates: array[InvoiceItemDueDatesOut] | null default=[]  // List of all due dates of the invoice.
  - attachments_info: ItemAttachmentInfoOut  // Indicates whether a file attachment (e.g. PDF or image) is linked to this invoice and how to retrieve it. Check the status field: 'yes' means a direct download URL is available in the attachments array; 'yes_to_request' means the file exists but must be fetched separately via GET /accounting/attachments?type=invoice&document_id={id}, which returns the file as a base64-encoded string. 'no' means no attachment is linked. 'unknown' means the connector does not support this.
  - accounting_info: AccountingInfoOut | null  // Additional information about the invoice.
  - payment_method_id: string | null  // Technical ID of the payment method in the accounting system. This is the payment method currently linked to the invoice. It is not necessarily the payment method that will eventually be used to pay the invoice.
  - approval_status: InvoiceApprovalStatus default="unknown"  // Approval status of the invoice.
  - lines *: array[InvoiceLineItemOutMultiAnalyticPlans]  // 

#### schema InvoiceType
  enum ['customer_invoice', 'customer_refund', 'supplier_invoice', 'supplier_refund']

#### schema WithholdingTax
  - tax_rate *: number  // Rate of the withholding tax. Normal withholding tax should have a negative tax rate.
  - tax_code *: string  // Tax code of the withholding tax. This is the Id of the Tax Code in the accounting software.
  - tax_amount *: number  // Amount of the withholding tax. This is the amount of the withholding tax that will be applied to the invoice. It should be negative for normal withholding tax.

#### schema Payment
  - id *: string  // 
  - name *: string  // 
  - currency *: string  // 
  - amount *: number  // Total amount of the payment. A part of this amount could be reconciled with another invoice.
  - dedicated_amount: number default=0  // Amount of the payment dedicated to the invoice. 
  - payment_date *: string(date)  // 
  - journal_type *: JournalType  // 
  - journal_id *: string  // 
  - journal_name *: string  // 
  - reconciled: boolean | null default=false  // 
  - communication: string | null  // 
  - matching_number: string | null  // 

#### schema JournalType
  enum ['customer_invoice', 'customer_refund', 'supplier_invoice', 'supplier_refund', 'financial_operation', 'miscellaneous_operation', 'unknown']

#### schema InvoiceStatusOut
  enum ['cancelled', 'draft', 'posted', 'paid']

#### schema Partner
  - external_reference: string | null  // External identifier used to link the client in the accounting system with the corresponding client reference in your own system.
  - first_name: string | null  // Only used when the client is an individual (is_company=false). Indicates the first name of the client.
  - last_name: string | null  // Only used when the client is an individual (is_company=false). Indicates the last name of the client.
  - name: string | null  // Full name or legal name of the client (individual or company). This is the name displayed in the accounting software.
  - function: string | null  // Only used when the client is an individual (is_company=false). Indicates the function of the client.
  - is_company: boolean | null default=true  // Indicates if the client is an individual or a company.
  - company_id: string | null  // Only used when the client is an individual (is_company=false). Indicates the id of the company linked to the client.
  - phone: string | null  // Phone number of the client.
  - mobile: string | null  // Mobile phone number of the client.
  - email: string | null  // Email address of the client.
  - language: string | null  // Language of the client. Format: ISO 639-1 codes.
  - internal_notes: string | null  // Internal notes about the client.
  - website: string | null  // Website of the client.
  - vat: string | null  // VAT number of the client.
  - company_number: string | null  // National identification number of the company.
  - iban: string | null  // IBAN account number of the client. DEPRECATED see bank_accounts
  - bank_account: string | null  // Bank account number of the client. DEPRECATED see bank_accounts
  - currency: string | null  // Indicates the currency of the client (e.g., EUR).
  - active: boolean | null default=true  // Indicates if the client is active.
  - account_number: string | null  // Ledger account number assigned to the customer in the accounting system as it will appear in the official accounting export file (FEC, SIE, iXBRL, etc.).
  - id: string | null  // Id of the client in the accounting software. This is the unique identifier used to reference the client in the system.
  - last_updated_on: string(date-time) | null  // The last time the client has been updated.
  - addresses: array[AddressItemOut] | null default=[]  // List of addresses associated with the client.
  - third_party_account: string | null  // Third party account number/code representing the client in the accounting software.
  - bank_accounts: array[BankAccountsItem] | null  // List of bank accounts information associated with the client.

#### schema AddressItemOut
  - address_type *: AddressType  // 
  - name: string | null  // 
  - number: string | null  // 
  - box: string | null  // 
  - phone: string | null  // 
  - mobile: string | null  // 
  - email: string | null  // 
  - street: string | null  // 
  - city: string | null  // 
  - postal_code: string | null  // 
  - country: string | null  // Format: ISO 3166-1 codes.

#### schema AddressType
  enum ['main', 'delivery', 'invoice']

#### schema BankAccountsItem
  - is_primary: boolean | null default=true  // Indicates whether this is the default bank account for this third-party. Only one bank account per third-party can have is_primary set to true. Defaults to true.
  - currency: string | null  // Indicates the currency of the bank account (e.g., EUR).
  - iban: string | null  // International Bank Account Number (ISO 13616). Present for countries in the IBAN scheme (e.g., France, Germany, United Kingdom). null for countries that do not participate in the IBAN scheme (e.g., US, Canada, Australia).
  - bic_swift: string | null  // Bank Identifier Code (ISO 9362), also known as SWIFT code. 8 or 11 characters. Optional for domestic payments, but required for international wire transfers.
  - account_number: string | null  // Local bank account number. Used when the country does not participate in the IBAN scheme (e.g., US, CA, AU). Always paired with a routing_code.
  - routing_code: RoutingCodeItem | null  // Domestic routing identifier for the bank. Required when no iban is present. Contains two subfields: type and value

#### schema RoutingCodeItem
  - type: BankAccountRoutingType default="unknown"  // The routing format. Possible values: ach (US), sort_code (UK), bsb (AU), transit (CA), ifsc (IN), clabe (MX).
  - value: string | null  // The raw routing code value, without spaces or dashes.

#### schema BankAccountRoutingType
  enum ['unknown', 'ach', 'sort_code', 'bsb', 'transit', 'ifsc', 'clabe']

#### schema InvoiceItemDueDatesOut
  - due_date *: string(date)  // Due date of the item.
  - payment_method: string | null  // Payment method used to pay the invoice on that due date.
  - payment_method_id: string | null  // Technical ID of the payment method used to pay the invoice on that due date.
  - amount *: number  // Amount due for the invoice on that due date. A positive amount represents debit on customer invoices and supplier refunds or credit on supplier invoices and customer refunds. A negative amount represents credit on customer invoices and supplier refunds or debit on supplier invoices and customer refunds.

#### schema ItemAttachmentInfoOut
  - status *: ItemAttachmentInfoStatus  // Indicates whether an attachment (e.g. PDF or image) is available for this entry, and how to retrieve it. 'yes': one or more attachments are available directly — each entry in the attachments array contains a filename and a download URL. 'yes_to_request': an attachment exists but cannot be returned inline. Call GET /accounting/attachments with type and document_id to retrieve the file as a base64-encoded string. The attachments array may be empty in this case. 'no': no attachment is linked to this entry. 'unknown': the connector does not support attachment detection for this provider.
  - attachments: array[ItemAttachmentInfoAttachment] | null default=[]  // List of attachments available directly for this entry. Populated only when status is 'yes'. When status is 'yes_to_request', this list is empty — use GET /accounting/attachments to fetch the file content.

#### schema ItemAttachmentInfoStatus
  enum ['unknown', 'yes', 'yes_to_request', 'no']

#### schema ItemAttachmentInfoAttachment
  - filename: string | null  // The name of the attachment.
  - url: string | null  // Direct download URL for the attachment file. Only populated when the parent attachments_info.status is 'yes'. When status is 'yes_to_request', this field is null and the file must be retrieved via GET /accounting/attachments with the appropriate type and document_id, which returns the content as a base64-encoded string.

#### schema AccountingInfoOut
  - main_currency: string  // Main currency of the accounting folder. ISO-4217 format.
  - main_currency_total: number default=0  // Total amount of the invoice in the accounting folder's currency.
  - account_number: string | null  // Client/supplier ledger account used to book the invoice total amount. (optional)

#### schema InvoiceApprovalStatus
  enum ['unknown', 'pending', 'approved', 'rejected']

#### schema InvoiceLineItemOutMultiAnalyticPlans
  - line_number: integer | null default=1  // Optional line sequence number used to preserve the order of invoice items.
  - unit_price *: number  // Unit price of the item, before tax.
  - unit_of_measure: string | null  // A list of default units can be used for which an advanced mapping has been done (units: 'hour', 'day', 'cm', 'm2', 'm3', 'm', 'km', 'mile', 'g', 'kg', 'ton', 'box', 'pallet', 'roll', 'liter', 'unit'). Custom units of measure must have an identical name in the target software.
  - quantity *: number  // Quantity of items. This is the amount of units sold or purchased.
  - untaxed_amount *: number  // Amount excluding tax for the line item (i.e., unit_price × quantity).
  - tax_rate *: number  // Tax rate used for the line (e.g., 21.0).
  - tax_amount *: number  // Tax amount calculated for the line (i.e. untaxed_amount * tax_rate).
  - total *: number  // Total amount for the item, including tax (untaxed_amount + tax_amount).
  - account_number: string | null  // Ledger account number (of type general) used for the line (e.g., 701000).
  - tax_code: string | null  // Indicates the tax code used for the line. This is the Id of the Tax Code in the accounting software.
  - description: string | null default=""  // Text description for this line.
  - analytic_distribution: array[AnalyticDistribution] | null default=[]  // List of analytic distributions for the line item. Each distribution specifies an analytic plan and the associated analytic accounts with their percentages.

#### schema AnalyticDistribution
  - analytic_plan *: string  // Id of the analytic plan to which the distribution applies.
  - analytic_accounts *: array[AnalyticDistributionDetail]  // List of analytic accounts and their respective percentages for the distribution.

#### schema AnalyticDistributionDetail
  - analytic_account *: string  // 
  - percentage *: number  // Percentage of the untaxed amount attributed to this analytic account. Only whole numbers (no decimals) are allowed. The total across the analytic distribution (all accounts in a given analytic plan) must equal 100%.
RESPONSE 400: Bad Request -> ChiftError
RESPONSE 422: Validation Error -> HTTPValidationError

====================================================================================================
## GET /consumers/{consumer_id}/accounting/journals
summary: Get journals
operationId: accounting_get_journals
description: Get journals existing in the accounting system
  param[path] consumer_id *: string(uuid) // 
  param[query] page: integer default=1 // Page number
  param[query] size: integer default=50 // Page size
  param[query] folder_id: string | null // Id of the accounting folder instance. A folder represents a legal entity within the system. Required when the multiple folders feature is enabled.
RESPONSE 200: Successful Response -> ChiftPage_Journal_

#### schema ChiftPage_Journal_
  - items *: array[Journal]  // 
  - total *: integer  // 
  - page *: integer  // 
  - size *: integer  // 

#### schema Journal
  - id *: string  // 
  - code: string | null  // 
  - name *: string  // 
  - journal_type *: JournalType  // 
  - counterpart_account: string | null  // When journal is of type bank or cash, this is account number of the counterpart account used for the journal.
  - unallocated_account: string | null  // Unallocated ledger account used to book entries when the final ledger account / client / supplier / employee is not yet known (specific to bank and cash journals)
  - next_document_numbers: array[NextDocumentNumber] | null default=[]  // 
  - iban: string | null  // When the journal is of type bank, IBAN of the bank account linked to the journal 
  - currency: string | null  // Currency of the journal (e.g., EUR). If empty, the journal follows the currency of the accounting folder.
  - other_currencies_allowed: boolean | null default=true  // Indicates if the journal allows other currencies. If it doesn't allow other currencies an exchange rate must be provided for Chift to convert the amounts to the journal currency. This only applicable if the journal currency is the same as the accounting folder currency.
  - blocked: boolean | null default=false  // Indicates if the journal is blocked for creating entries.

#### schema JournalType
  enum ['customer_invoice', 'customer_refund', 'supplier_invoice', 'supplier_refund', 'financial_operation', 'miscellaneous_operation', 'unknown']

#### schema NextDocumentNumber
  - bookyear_name: string | null  // 
  - next_document_number: string | null  // 
  - start_date: string(date) | null  // 
  - end_date: string(date) | null  // 
RESPONSE 400: Bad Request -> ChiftError
RESPONSE 422: Validation Error -> HTTPValidationError

====================================================================================================
## POST /consumers/{consumer_id}/accounting/accounts
summary: Create ledger account
operationId: accounting_create_ledger_account
description: Create a new ledger account in the chart of accounts
  param[path] consumer_id *: string(uuid) // 
  param[query] folder_id: string | null // Id of the accounting folder instance. A folder represents a legal entity within the system. Required when the multiple folders feature is enabled.
REQUEST BODY: LedgerAccountItemIn | required

#### schema LedgerAccountItemIn
  - name *: string  // Name or label of the ledger account as it appears in the accounting system.
  - number *: string  // The account number in the chart of accounts. Must be unique within the accounting folder. In some countries (e.g., France, Belgium, Spain), the number structure is constrained by local accounting rules and must follow official charts of accounts (e.g., Plan Comptable Général).
  - type: AccountItemType | null default="other"  // 

#### schema AccountItemType
  enum ['bank', 'cash', 'other_financial', 'receivable', 'payable', 'income', 'expense', 'other_expense', 'vat', 'other']
RESPONSE 200: Successful Response -> AccountItem

#### schema AccountItem
  - number *: string  // The account number in the chart of accounts. Must be unique within the accounting folder. In some countries (e.g., France, Belgium, Spain), the number structure is constrained by local accounting rules and must follow official charts of accounts (e.g., Plan Comptable Général).
  - name *: string  // Name or label of the account as it appears in the accounting system. This is typically used for internal referencing and identification of the account.
  - active: boolean | null default=true  // Flag indicating whether the account is active. If True, the account is active and can be used in transactions. If False, the account is inactive and cannot be used for transactions.
  - type: AccountItemType | null  // Represents the functional type of the ledger account, used to support common accounting operations such as payments, invoicing, tax handling, and reporting. The type here is more operational and aligned with how accounts are actually used in day-to-day processes (e.g., tracking receivables, recording VAT, handling bank transactions) 
  - scheme_ids: array[string] | null  // List of scheme classification IDs linked to this ledger account. A scheme (e.g., RGS, SBR) provides a standardized classification structure for organizing accounts for reporting purposes. Multiple scheme codes can be associated with a single account.
  - accounting_category: string | null  // Category of the ledger account in the accounting system. This is the category of the account as defined in the accounting system.
RESPONSE 400: Bad Request -> ChiftError
RESPONSE 422: Validation Error -> HTTPValidationError

====================================================================================================
## GET /consumers/{consumer_id}/accounting/chart-of-accounts
summary: Get chart of accounts
operationId: accounting_get_chart_of_accounts
description: Get all accounts in the chart of accounts
  param[path] consumer_id *: string(uuid) // 
  param[query] page: integer default=1 // Page number
  param[query] size: integer default=50 // Page size
  param[query] folder_id: string | null // Id of the accounting folder instance. A folder represents a legal entity within the system. Required when the multiple folders feature is enabled.
  param[query] classes: string | null // Filter based on the class of the account (e.g. 6,7 to retrieve 6 and 7 account classes). The classes are separated by ','.
  param[query] type: AccountTypeFilter | null // Filter based on the type of the account (e.g. bank, cash, income, expense, vat).
RESPONSE 200: Successful Response -> ChiftPage_AccountItem_

#### schema ChiftPage_AccountItem_
  - items *: array[AccountItem]  // 
  - total *: integer  // 
  - page *: integer  // 
  - size *: integer  // 

#### schema AccountItem
  - number *: string  // The account number in the chart of accounts. Must be unique within the accounting folder. In some countries (e.g., France, Belgium, Spain), the number structure is constrained by local accounting rules and must follow official charts of accounts (e.g., Plan Comptable Général).
  - name *: string  // Name or label of the account as it appears in the accounting system. This is typically used for internal referencing and identification of the account.
  - active: boolean | null default=true  // Flag indicating whether the account is active. If True, the account is active and can be used in transactions. If False, the account is inactive and cannot be used for transactions.
  - type: AccountItemType | null  // Represents the functional type of the ledger account, used to support common accounting operations such as payments, invoicing, tax handling, and reporting. The type here is more operational and aligned with how accounts are actually used in day-to-day processes (e.g., tracking receivables, recording VAT, handling bank transactions) 
  - scheme_ids: array[string] | null  // List of scheme classification IDs linked to this ledger account. A scheme (e.g., RGS, SBR) provides a standardized classification structure for organizing accounts for reporting purposes. Multiple scheme codes can be associated with a single account.
  - accounting_category: string | null  // Category of the ledger account in the accounting system. This is the category of the account as defined in the accounting system.

#### schema AccountItemType
  enum ['bank', 'cash', 'other_financial', 'receivable', 'payable', 'income', 'expense', 'other_expense', 'vat', 'other']
RESPONSE 400: Bad Request -> ChiftError
RESPONSE 422: Validation Error -> HTTPValidationError

====================================================================================================
## GET /consumers/{consumer_id}/accounting/folders
summary: Get Folders
operationId: accounting_get_folders
  param[path] consumer_id *: string(uuid) // 
RESPONSE 200: Successful Response -> array[FolderItem]

#### schema FolderItem
  - id *: string  // 
  - name *: string  // 
  - selected: boolean | null default=true  // Indicates whether the folder was selected during the Chift activation process. Only selected folders can be used in subsequent requests. Requests targeting a folder that was not selected will be rejected. If only one folder is selected, it will be used by default when no folder is specified in the request.
  - active: boolean | null default=true  // Indicates whether the folder is currently active in the target accounting software. Requests targeting an inactive folder will fail on the target software side.
  - vat: string | null  // 
  - company_number: string | null  // 
  - main_currency: string | null  // Format: ISO 3166-1 codes.
  - addresses: array[FolderAddressItem] | null  // 

#### schema FolderAddressItem
  - street: string | null  // 
  - number: string | null  // 
  - box: string | null  // 
  - postal_code: string | null  // 
  - city: string | null  // 
  - country: string | null  // Format: ISO 3166-1 codes.
RESPONSE 400: Bad Request -> ChiftError
RESPONSE 422: Validation Error -> HTTPValidationError

====================================================================================================
## GET /consumers/{consumer_id}/accounting/analytic-plans
summary: Get Analytic Plans
operationId: accounting_get_analytic_plans
  param[path] consumer_id *: string(uuid) // 
  param[query] page: integer default=1 // Page number
  param[query] size: integer default=50 // Page size
  param[query] folder_id: string | null // Id of the accounting folder instance. A folder represents a legal entity within the system. Required when the multiple folders feature is enabled.
RESPONSE 200: Successful Response -> ChiftPage_AnalyticPlanItem_

#### schema ChiftPage_AnalyticPlanItem_
  - items *: array[AnalyticPlanItem]  // 
  - total *: integer  // 
  - page *: integer  // 
  - size *: integer  // 

#### schema AnalyticPlanItem
  - id *: string  // Unique id of the analytic plan instance in the accounting system.
  - name *: string  // Name of the analytic plan as it appears in the accounting system.
  - active: boolean | null default=true  // Indicates if the analytic plan is active.
  - parent_id: string | null  // Id of the parent analytic plan, if any. This is used to create a hierarchy of analytic plans when that is supported.
RESPONSE 400: Bad Request -> ChiftError
RESPONSE 422: Validation Error -> HTTPValidationError

====================================================================================================
## GET /consumers/{consumer_id}/accounting/analytic-accounts/multi-analytic-plans
summary: Get analytic accounts (Multiple Analytic Plans)
operationId: accounting_get_analytic_accounts_multi_plans
description: Returns all analytic accounts of all analytic plans
  param[path] consumer_id *: string(uuid) // 
  param[query] page: integer default=1 // Page number
  param[query] size: integer default=50 // Page size
  param[query] folder_id: string | null // Id of the accounting folder instance. A folder represents a legal entity within the system. Required when the multiple folders feature is enabled.
RESPONSE 200: Successful Response -> ChiftPage_AnalyticAccountItemOutMultiAnalyticPlans_

#### schema ChiftPage_AnalyticAccountItemOutMultiAnalyticPlans_
  - items *: array[AnalyticAccountItemOutMultiAnalyticPlans]  // 
  - total *: integer  // 
  - page *: integer  // 
  - size *: integer  // 

#### schema AnalyticAccountItemOutMultiAnalyticPlans
  - id *: string  // Unique id of the analytic account in the accounting system.
  - active *: boolean  // Flag indicating whether the analytic account is active.
  - code: string | null  // Short code for the analytic account. Often used for internal referencing. For some integrations, it may be required to be unique.
  - name *: string  // Name or label of the analytic account as it appears in the accounting system.
  - currency: string | null  // Indicates the currency of the analytic account (e.g., EUR, USD).
  - balance: number | null default=0  // 
  - credit: number | null default=0  // 
  - debit: number | null default=0  // 
  - analytic_plan *: string  // 
RESPONSE 400: Bad Request -> ChiftError
RESPONSE 422: Validation Error -> HTTPValidationError

====================================================================================================
## POST /consumers/{consumer_id}/accounting/miscellaneous-operation
summary: Create miscellaneous operation
operationId: accounting_create_miscellaneous_operation
description: Create a new miscellaneous operation
  param[path] consumer_id *: string(uuid) // 
  param[query] folder_id: string | null // Id of the accounting folder instance. A folder represents a legal entity within the system. Required when the multiple folders feature is enabled.
REQUEST BODY: MiscellaneousOperationIn | required

#### schema MiscellaneousOperationIn
  - operation_number: string | null  // 
  - currency *: string  // Indicates the currency of the operation (e.g., EUR, USD).
  - currency_exchange_rate: number | null default=1  // Indicates the exchange rate at the date of the operation. Must be filled in when creating the operation in another currency from the folder's default currency.
  - lines *: array[MiscellaneousOperationLine]  // 
  - operation_date *: string(date)  // 
  - journal_id: string | null  // Indicates the journal used in for the operation. If the journal is not given, the journal will be automatically set if only one journal exists otherwise an error will be thrown.
  - status: MiscellaneousOperationStatusIn | null default="posted"  // 

#### schema MiscellaneousOperationLine
  - line_number: integer | null default=1  // Line number of the operation line. This is used to order the lines in the operation. It is automatically set to 1 if not provided.
  - description: string | null  // Text description used to provide additional context or information about the operation line.
  - amount *: number  // Positive for Credit and negative for Debit.
  - type *: MiscellaneousOperationLineType  // 
  - account_number *: string  // Indicates the account number used in the operation line. This is the ledger account number in the chart of accounts.
  - partner_id: string | null  // Must be filled in if it is a 'customer_account' or 'supplier_account' line type.
  - analytic_account: string | null  // Analytic account used in the operation line. This is the id of a analytic account - no distribution possible. It is used to track the operation line in the analytic accounting system.

#### schema MiscellaneousOperationLineType
  enum ['customer_account', 'supplier_account', 'general_account']

#### schema MiscellaneousOperationStatusIn
  enum ['draft', 'posted']
RESPONSE 200: Successful Response -> MiscellaneousOperationOut

#### schema MiscellaneousOperationOut
  - operation_number: string | null  // 
  - currency *: string  // Indicates the currency of the operation (e.g., EUR, USD).
  - currency_exchange_rate: number | null default=1  // Indicates the exchange rate at the date of the operation. Must be filled in when creating the operation in another currency from the folder's default currency.
  - lines *: array[MiscellaneousOperationLine]  // 
  - operation_date: string(date) | null default="1970-01-01"  // Accounting date of the miscellaneous operation. It is automatically set to '1970-01-01' if the value is not available/empty in the accounting system.
  - journal_id *: string  // Indicates the journal used in for the operation.
  - status *: MiscellaneousOperationStatusOut  // 
  - id *: string  // 

#### schema MiscellaneousOperationStatusOut
  enum ['cancelled', 'draft', 'posted', 'matched']
RESPONSE 400: Bad Request -> ChiftError
RESPONSE 422: Unprocessable Entity -> ChiftError
RESPONSE 404: Not Found -> ChiftError

====================================================================================================
## GET /consumers/{consumer_id}/accounting/vat-codes
summary: Get vat codes
operationId: accounting_get_vat_codes
description: Get vat codes existing in the accounting system
  param[path] consumer_id *: string(uuid) // 
  param[query] page: integer default=1 // Page number
  param[query] size: integer default=50 // Page size
  param[query] folder_id: string | null // Id of the accounting folder instance. A folder represents a legal entity within the system. Required when the multiple folders feature is enabled.
RESPONSE 200: Successful Response -> ChiftPage_AccountingVatCode_

#### schema ChiftPage_AccountingVatCode_
  - items *: array[AccountingVatCode]  // 
  - total *: integer  // 
  - page *: integer  // 
  - size *: integer  // 

#### schema AccountingVatCode
  - id *: string  // Unique id of the VAT Code instance in the accounting system.
  - code: string | null  // Short code (sometimes also used as id) for the VAT code, as defined in the accounting system. This code is typically used for internal referencing, mapping, or selection of VAT codes
  - active: boolean | null default=true  // Flag indicating whether the vat code is active. If True, the vat code is active and can be used in entries/invoices. If False, the vat code is inactive and cannot be used in entries/invoices.
  - label *: string  // Label of the VAT code as it appears in the accounting system. This is the human-readable name used to identify the VAT code.
  - scope: VatCodeScope | null default="unknown"  // Scope of the VAT code, indicating its applicability. Use 'nat' for VAT codes that apply to local/domestic sales or purchases, 'eu' for cross-border transactions within the EU, and 'int' for transactions with countries outside the EU.
  - rate *: number  // VAT rate associated with the VAT code. This is the percentage rate applied to the amount when this VAT code is used.
  - type *: VatCodeType  // Type of the VAT code, indicating whether it is a sales tax or purchase tax. This helps in understanding how the VAT code is applied in transactions.
  - deductible_account: string | null  // Ledger account number used for the deductible part of the VAT code. This is typically used for purchase transactions where VAT can be deducted.
  - payable_account: string | null  // Ledger account number used for the payable part of the VAT code. This is typically used for sales transactions where VAT is collected from customers.
  - reversed: boolean | null default=false  // Indicates whether the VAT code is reversed. A reversed VAT code is used in specific scenarios, such as reverse charge mechanisms, where the responsibility for reporting VAT shifts from the seller to the buyer.
  - withholding_tax: boolean | null default=false  // Indicates whether the VAT code is a withholding tax. This is used to indicate that the VAT code is a withholding tax and should be treated as such.
  - country: string | null  // Country of the VAT code. This is the ISO 3166-1 code of the country.

#### schema VatCodeScope
  enum ['nat', 'eu', 'int', 'unknown']

#### schema VatCodeType
  enum ['sale', 'purchase', 'both', 'unknown']
RESPONSE 400: Bad Request -> ChiftError
RESPONSE 422: Validation Error -> HTTPValidationError

====================================================================================================
## GET /consumers/{consumer_id}/accounting/bookyears
summary: Get Bookyears
operationId: accounting_get_bookyears
  param[path] consumer_id *: string(uuid) // 
  param[query] page: integer default=1 // Page number
  param[query] size: integer default=50 // Page size
  param[query] folder_id: string | null // Id of the accounting folder instance. A folder represents a legal entity within the system. Required when the multiple folders feature is enabled.
RESPONSE 200: Successful Response -> ChiftPage_BookYear_

#### schema ChiftPage_BookYear_
  - items *: array[BookYear]  // 
  - total *: integer  // 
  - page *: integer  // 
  - size *: integer  // 

#### schema BookYear
  - name *: string  // Name of the book year, typically in the format 'YYYY'.
  - start *: string(date)  // Start date of the book year (format: YYYY-MM-DD). This is the date when the book year begins.
  - end *: string(date)  // End date of the book year (format: YYYY-MM-DD). This is the date when the book year ends.
  - closed *: boolean  // Indicates whether the book year is closed. A closed book year normally cannot be modified or have new entries added to it.
RESPONSE 400: Bad Request -> ChiftError
RESPONSE 422: Validation Error -> HTTPValidationError
```

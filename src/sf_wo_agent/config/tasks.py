from crewai import Task

def get_tasks():
    """Returns a dictionary of tasks initialized with their configurations."""
    tasks = {}

    tasks['account_update_speed_and_charge'] = Task(
        description=(
            "Maintain the current data rate and activation details for the customer's account and order. "
            "Ensure that this task is only executed if the account and order are up-to-date with the latest service information."
        ),
        expected_output=(
            "The output will be a JSON object containing the order number and account details, such as Id, AccountName, "
            "AccountStatus, and OrderStatus. Additionally, an OrchestrationItems list will be included where each item captures "
            "details like OrchestrationItemType, OrchestrationPlanId, Name, DependsOnItemId, OrchestrationItemName, "
            "OrchestrationItemState, and CreatedDate."
        )
    )

    tasks['create_account_contact_updates'] = Task(
        description=(
            "Process necessary updates to account and contact information based on recent changes or new information received. "
            "Ensure that all related tasks for account and contact updates are completed before this task proceeds."
        ),
        expected_output=(
            "The output will be a JSON object structured to include the order number and related account details. The OrchestrationItems list "
            "will include entries with fields such as OrchestrationItemType, OrchestrationPlanId, Name, DependsOnItemId, "
            "OrchestrationItemName, OrchestrationItemState, and CreatedDate."
        )
    )

    tasks['update_wo_and_sa'] = Task(
        description=(
            "Create Work Order and Service Appointment records. This task can proceed independently as it does not rely on other tasks."
        ),
        expected_output=(
            "The output will be a JSON object containing the order number and account details, such as Id, AccountName, AccountStatus, "
            "and OrderStatus. Additionally, an OrchestrationItems list will be included where each item captures details like "
            "OrchestrationItemType, OrchestrationPlanId, Name, DependsOnItemId, OrchestrationItemName, OrchestrationItemState, and CreatedDate."
        )
    )

    tasks['update_wo_facilities'] = Task(
        description=(
            "Fetch facilities data needed for technician provisioning. This task can proceed independently as it does not rely on other tasks."
        ),
        expected_output=(
            "The output will be a JSON object containing the order number and account details, such as Id, AccountName, AccountStatus, "
            "and OrderStatus. Additionally, an OrchestrationItems list will be included where each item captures details like "
            "OrchestrationItemType, OrchestrationPlanId, Name, DependsOnItemId, OrchestrationItemName, OrchestrationItemState, and CreatedDate."
        )
    )

    tasks['get_and_activate_dtn'] = Task(
        description=(
            "Retrieve and activate the DTN. Ensure that prerequisite setup tasks related to DTN are completed before proceeding. "
            "This task will not execute if DTN setup is incomplete."
        ),
        expected_output=(
            "The output will be a JSON object containing the order number and account details, such as Id, AccountName, AccountStatus, "
            "and OrderStatus. Additionally, an OrchestrationItems list will be included where each item captures details like "
            "OrchestrationItemType, OrchestrationPlanId, Name, DependsOnItemId, OrchestrationItemName, OrchestrationItemState, and CreatedDate."
        )
    )

    tasks['get_health_certificate'] = Task(
        description=(
            "Check the health of the internet speed and create a health certificate record. This task is independent and can proceed regardless of the state of other tasks."
        ),
        expected_output=(
            "The output will be a JSON object containing the order number and account details, such as Id, AccountName, AccountStatus, "
            "and OrderStatus. Additionally, an OrchestrationItems list will be included where each item captures details like "
            "OrchestrationItemType, OrchestrationPlanId, Name, DependsOnItemId, OrchestrationItemName, OrchestrationItemState, and CreatedDate."
        )
    )

    tasks['acs_on_reset_gateway'] = Task(
        description=(
            "Make an API call to ACS system to reset the Active modem device. This task depends on the completion of device setup tasks. "
            "It will not execute if device setup is incomplete."
        ),
        expected_output=(
            "The output will be a JSON object containing the order number and account details, such as Id, AccountName, AccountStatus, "
            "and OrderStatus. Additionally, an OrchestrationItems list will be included where each item captures details like "
            "OrchestrationItemType, OrchestrationPlanId, Name, DependsOnItemId, OrchestrationItemName, OrchestrationItemState, and CreatedDate."
        )
    )

    tasks['acs_smartnid_reset_gateway'] = Task(
        description=(
            "Reset the smartnid device modem. Ensure that device setup tasks are completed before proceeding. "
            "This task will not execute if device setup is incomplete."
        ),
        expected_output=(
            "The output will be a JSON object containing the order number and account details, such as Id, AccountName, AccountStatus, "
            "and OrderStatus. Additionally, an OrchestrationItems list will be included where each item captures details like "
            "OrchestrationItemType, OrchestrationPlanId, Name, DependsOnItemId, OrchestrationItemName, OrchestrationItemState, and CreatedDate."
        )
    )

    tasks['assia_on_update_speed'] = Task(
        description=(
            "Make an API call to IMPROV system to update the speed. This task requires all related speed change requests to be completed before it can proceed."
        ),
        expected_output=(
            "The output will be a JSON object containing the order number and account details, such as Id, AccountName, AccountStatus, "
            "and OrderStatus. Additionally, an OrchestrationItems list will be included where each item captures details like "
            "OrchestrationItemType, OrchestrationPlanId, Name, DependsOnItemId, OrchestrationItemName, OrchestrationItemState, and CreatedDate."
        )
    )

    tasks['assia_speed_update'] = Task(
        description=(
            "Upgrade or downgrade the internet speed. Ensure all related speed management tasks are completed before proceeding."
        ),
        expected_output=(
            "The output will be a JSON object containing the order number and account details, such as Id, AccountName, AccountStatus, "
            "and OrderStatus. Additionally, an OrchestrationItems list will be included where each item captures details like "
            "OrchestrationItemType, OrchestrationPlanId, Name, DependsOnItemId, OrchestrationItemName, OrchestrationItemState, and CreatedDate."
        )
    )

    tasks['create_zuora_subscription'] = Task(
        description=(
            "Create a subscription in Zuora. This task requires completion of all setup tasks for subscription creation."
        ),
        expected_output=(
            "The output will be a JSON object containing the order number and account details, such as Id, AccountName, AccountStatus, "
            "and OrderStatus. Additionally, an OrchestrationItems list will be included where each item captures details like "
            "OrchestrationItemType, OrchestrationPlanId, Name, DependsOnItemId, OrchestrationItemName, OrchestrationItemState, and CreatedDate."
        )
    )

    tasks['fiber_provisioning_modified'] = Task(
        description=(
            "Provision fiber service for a migrated customer. Ensure necessary setup and provisioning tasks are completed before proceeding."
        ),
        expected_output=(
            "The output will be a JSON object containing the order number and account details, such as Id, AccountName, AccountStatus, "
            "and OrderStatus. Additionally, an OrchestrationItems list will be included where each item captures details like "
            "OrchestrationItemType, OrchestrationPlanId, Name, DependsOnItemId, OrchestrationItemName, OrchestrationItemState, and CreatedDate."
        )
    )

    tasks['hsi_fiber_assetize'] = Task(
        description=(
            "Create assets using Assetize Auto task. This task can proceed independently as it does not rely on other tasks."
        ),
        expected_output=(
            "The output will be a JSON object containing the order number and account details, such as Id, AccountName, AccountStatus, "
            "and OrderStatus. Additionally, an OrchestrationItems list will be included where each item captures details like "
            "OrchestrationItemType, OrchestrationPlanId, Name, DependsOnItemId, OrchestrationItemName, OrchestrationItemState, and CreatedDate."
        )
    )

    tasks['improv_on_remove_dtn_from_walled'] = Task(
        description=(
            "Remove DTN from walled garden for ON customer. Ensure related DTN management tasks are completed before proceeding."
        ),
        expected_output=(
            "The output will be a JSON object containing the order number and account details, such as Id, AccountName, AccountStatus, "
            "and OrderStatus. Additionally, an OrchestrationItems list will be included where each item captures details like "
            "OrchestrationItemType, OrchestrationPlanId, Name, DependsOnItemId, OrchestrationItemName, OrchestrationItemState, and CreatedDate."
        )
    )

    tasks['improv_speed_change'] = Task(
        description=(
            "Make an API call to IMPROV system to change speed. This task requires all related speed management tasks to be completed before it can proceed."
        ),
        expected_output=(
            "The output will be a JSON object containing the order number and account details, such as Id, AccountName, AccountStatus, "
            "and OrderStatus. Additionally, an OrchestrationItems list will be included where each item captures details like "
            "OrchestrationItemType, OrchestrationPlanId, Name, DependsOnItemId, OrchestrationItemName, OrchestrationItemState, and CreatedDate."
        )
    )

    tasks['optius_on_reset_speed'] = Task(
        description=(
            "Callout to reset speed for Fiber customer. Ensure related setup tasks are completed before this task can proceed."
        ),
        expected_output=(
            "The output will be a JSON object containing the order number and account details, such as Id, AccountName, AccountStatus, "
            "and OrderStatus. Additionally, an OrchestrationItems list will be included where each item captures details like "
            "OrchestrationItemType, OrchestrationPlanId, Name, DependsOnItemId, OrchestrationItemName, OrchestrationItemState, and CreatedDate."
        )
    )

    tasks['optius_on_update_speed'] = Task(
        description=(
            "Callout to update speed for customer order product. This task depends on the completion of related speed update tasks."
        ),
        expected_output=(
            "The output will be a JSON object containing the order number and account details, such as Id, AccountName, AccountStatus, "
            "and OrderStatus. Additionally, an OrchestrationItems list will be included where each item captures details like "
            "OrchestrationItemType, OrchestrationPlanId, Name, DependsOnItemId, OrchestrationItemName, OrchestrationItemState, and CreatedDate."
        )
    )

    tasks['oss_fiber_speed_change'] = Task(
        description=(
            "Callout to reset speed for Fiber customer. This task requires completion of related setup tasks."
        ),
        expected_output=(
            "The output will be a JSON object containing the order number and account details, such as Id, AccountName, AccountStatus, "
            "and OrderStatus. Additionally, an OrchestrationItems list will be included where each item captures details like "
            "OrchestrationItemType, OrchestrationPlanId, Name, DependsOnItemId, OrchestrationItemName, OrchestrationItemState, and CreatedDate."
        )
    )

    tasks['oss_instantwifi_speed_change'] = Task(
        description=(
            "Callout to reset speed for Instant Wifi customer. Ensure all related tasks are completed before proceeding."
        ),
        expected_output=(
            "The output will be a JSON object containing the order number and account details, such as Id, AccountName, AccountStatus, "
            "and OrderStatus. Additionally, an OrchestrationItems list will be included where each item captures details like "
            "OrchestrationItemType, OrchestrationPlanId, Name, DependsOnItemId, OrchestrationItemName, OrchestrationItemState, and CreatedDate."
        )
    )

    tasks['oss_optius_fiber_activation_new_customer'] = Task(
        description=(
            "Activate fiber internet service for a new customer. This task depends on the completion of all prerequisite tasks for fiber activation."
        ),
        expected_output=(
            "The output will be a JSON object containing the order number and account details, such as Id, AccountName, AccountStatus, "
            "and OrderStatus. Additionally, an OrchestrationItems list will be included where each item captures details like "
            "OrchestrationItemType, OrchestrationPlanId, Name, DependsOnItemId, OrchestrationItemName, OrchestrationItemState, and CreatedDate."
        )
    )

    tasks['oss_voice_activation_existing_customer'] = Task(
        description=(
            "Activate voice service for an existing fiber customer. Ensure all related voice service activation tasks are completed before proceeding."
        ),
        expected_output=(
            "The output will be a JSON object containing the order number and account details, such as Id, AccountName, AccountStatus, "
            "and OrderStatus. Additionally, an OrchestrationItems list will be included where each item captures details like "
            "OrchestrationItemType, OrchestrationPlanId, Name, DependsOnItemId, OrchestrationItemName, OrchestrationItemState, and CreatedDate."
        )
    )

    tasks['update_improv_for_smartnid'] = Task(
        description=(
            "Update the DTN status in the IMPROV system. Ensure related DTN management tasks are completed before proceeding."
        ),
        expected_output=(
            "The output will be a JSON object containing the order number and account details, such as Id, AccountName, AccountStatus, "
            "and OrderStatus. Additionally, an OrchestrationItems list will be included where each item captures details like "
            "OrchestrationItemType, OrchestrationPlanId, Name, DependsOnItemId, OrchestrationItemName, OrchestrationItemState, and CreatedDate."
        )
    )

    tasks['update_optius_for_smartnid'] = Task(
        description=(
            "Update the Optius system asynchronously for SmartNID. Ensure all related setup tasks are completed before this task can proceed."
        ),
        expected_output=(
            "The output will be a JSON object containing the order number and account details, such as Id, AccountName, AccountStatus, "
            "and OrderStatus. Additionally, an OrchestrationItems list will be included where each item captures details like "
            "OrchestrationItemType, OrchestrationPlanId, Name, DependsOnItemId, OrchestrationItemName, OrchestrationItemState, and CreatedDate."
        )
    )

    tasks['update_optius_for_smartnid_disconnect'] = Task(
        description=(
            "Create a change order in Optius for SmartNID disconnect. Ensure related disconnect tasks are completed before proceeding."
        ),
        expected_output=(
            "The output will be a JSON object containing the order number and account details, such as Id, AccountName, AccountStatus, "
            "and OrderStatus. Additionally, an OrchestrationItems list will be included where each item captures details like "
            "OrchestrationItemType, OrchestrationPlanId, Name, DependsOnItemId, OrchestrationItemName, OrchestrationItemState, and CreatedDate."
        )
    )

    tasks['create_smartnid_disconnect_order_for_current_customer'] = Task(
        description=(
            "Create a disconnect order for SmartNID for a current customer. This task can proceed independently as it does not rely on other tasks."
        ),
        expected_output=(
            "The output will be a JSON object containing the order number and account details, such as Id, AccountName, AccountStatus, "
            "and OrderStatus. Additionally, an OrchestrationItems list will be included where each item captures details like "
            "OrchestrationItemType, OrchestrationPlanId, Name, DependsOnItemId, OrchestrationItemName, OrchestrationItemState, and CreatedDate."
        )
    )

    tasks['create_migration'] = Task(
        description=(
            "Create a migration conflict case. This task can proceed independently as it does not rely on other tasks."
        ),
        expected_output=(
            "The output will be a JSON object containing the order number and account details, such as Id, AccountName, AccountStatus, "
            "and OrderStatus. Additionally, an OrchestrationItems list will be included where each item captures details like "
            "OrchestrationItemType, OrchestrationPlanId, Name, DependsOnItemId, OrchestrationItemName, OrchestrationItemState, and CreatedDate."
        )
    )

    tasks['migration_modem_replacement_case_creation'] = Task(
        description=(
            "Create a case for modem replacement shipment for migrated customer orders. This task can proceed independently as it does not rely on other tasks."
        ),
        expected_output=(
            "The output will be a JSON object containing the order number and account details, such as Id, AccountName, AccountStatus, "
            "and OrderStatus. Additionally, an OrchestrationItems list will be included where each item captures details like "
            "OrchestrationItemType, OrchestrationPlanId, Name, DependsOnItemId, OrchestrationItemName, OrchestrationItemState, and CreatedDate."
        )
    )

    tasks['waiting_on_customer_confirmation'] = Task(
        description=(
            "Send an email to the customer when there is a change in the service appointment. Ensure all related tasks are completed before sending the confirmation."
        ),
        expected_output=(
            "The output will be a JSON object containing the order number and account details, such as Id, AccountName, AccountStatus, "
            "and OrderStatus. Additionally, an OrchestrationItems list will be included where each item captures details like "
            "OrchestrationItemType, OrchestrationPlanId, Name, DependsOnItemId, OrchestrationItemName, OrchestrationItemState, and CreatedDate."
        )
    )

    tasks['oss_optius_work_order_sign_off'] = Task(
        description=(
            "Sign off the work order upon completion. Ensure all related tasks are completed before signing off."
        ),
        expected_output=(
            "The output will be a JSON object containing the order number and account details, such as Id, AccountName, AccountStatus, "
            "and OrderStatus. Additionally, an OrchestrationItems list will be included where each item captures details like "
            "OrchestrationItemType, OrchestrationPlanId, Name, DependsOnItemId, OrchestrationItemName, OrchestrationItemState, and CreatedDate."
        )
    )

    tasks['migrate_oss_optius_work_order_sign_off'] = Task(
        description=(
            "Sign off the work order from a technician when the order is completed. Ensure all related tasks are completed before technician sign-off."
        ),
        expected_output=(
            "The output will be a JSON object containing the order number and account details, such as Id, AccountName, AccountStatus, "
            "and OrderStatus. Additionally, an OrchestrationItems list will be included where each item captures details like "
            "OrchestrationItemType, OrchestrationPlanId, Name, DependsOnItemId, OrchestrationItemName, OrchestrationItemState, and CreatedDate."
        )
    )

    return tasks
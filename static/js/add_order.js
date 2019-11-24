function setCustomerDetails(customer){

    var ddl = document.getElementById("cust_id");
    var selectedOption = ddl.options[ddl.selectedIndex];
    var phone = selectedOption.getAttribute("id");


    var phone_number = document.getElementById("phone_number");
    var first_name = document.getElementById("first_name");
    var last_name = document.getElementById("last_name");
    var customer_remarks = document.getElementById("customer_remarks");


    for(var i = 1; i < customer.length; i++) {
        var obj = customer[i];
        if (obj.phone_number == phone){
            phone_number.value = obj.phone_number;
            document.getElementById("phone_number").readOnly = true;
            first_name.value = obj.first_name;
            document.getElementById("first_name").readOnly = true;
            last_name.value = obj.last_name;
            document.getElementById("last_name").readOnly = true;
            customer_remarks.value = obj.customer_remarks;
            document.getElementById("customer_remarks").readOnly = true;
            if (obj.gender == "male")
                document.getElementById("male").checked = true;
            else
                document.getElementById("female").checked = true;
            document.getElementById("male").readOnly = true;
            document.getElementById("female").readOnly = true;
        }
    }
    var obj = customer[0];
        if (obj.phone_number == phone){
            phone_number.value = "";
            document.getElementById("phone_number").readOnly = false;
            first_name.value = "";
            document.getElementById("first_name").readOnly = false;
            last_name.value = "";
            document.getElementById("last_name").readOnly = false;
            customer_remarks.value = "";
            document.getElementById("customer_remarks").readOnly = false;
            if (obj.gender == "male")
                document.getElementById("male").checked = false;
            else
                document.getElementById("female").checked = false;
            document.getElementById("male").readOnly = false;
            document.getElementById("female").readOnly = false;
        }

}
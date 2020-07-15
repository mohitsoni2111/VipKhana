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




function setAddressDetails(address){

    var ddl = document.getElementById("adr_id");
    var selectedOption = ddl.options[ddl.selectedIndex];
    var address_id = selectedOption.getAttribute("id");

    var line1 = document.getElementById("line1");
    var line2 = document.getElementById("line2");
    var line3 = document.getElementById("line3");
    var address_remarks = document.getElementById("address_remarks");

    for(var i = 1; i < address.length; i++) {
        var obj = address[i];
        if (obj._id == address_id){
            line1.value = obj.line1;
            document.getElementById("line1").readOnly = true;
            line2.value = obj.line2;
            document.getElementById("line2").readOnly = true;
            line3.value = obj.line3;
            document.getElementById("line3").readOnly = true;
            address_remarks.value = obj.address_remarks;
            document.getElementById("address_remarks").readOnly = true;
        }
    }
    var obj = address[0];
        if (obj._id == address_id){
            line1.value = "";
            document.getElementById("line1").readOnly = false;
            line2.value = "";
            document.getElementById("line2").readOnly = false;
            line3.value = "";
            document.getElementById("line3").readOnly = false;
            address_remarks.value = "";
            document.getElementById("address_remarks").readOnly = false;
        }
}



function setLocalityDetails(locality_list){
    var ddl = document.getElementById("loc_id");
    var selectedOption = ddl.options[ddl.selectedIndex];
    var locality_id = selectedOption.getAttribute("id");

    var locality = document.getElementById("locality");

    for(var i = 1; i < locality_list.length; i++) {
        var obj = locality_list[i];
        if (obj._id == locality_id){
            locality.value = obj.name;
            document.getElementById("locality").readOnly = true;
        }
    }
    var obj = locality_list[0];
        if (obj._id == locality_id){
            locality.value = "";
            document.getElementById("locality").readOnly = false;
        }
}


function setExpenseClassDetails(expense_class_list){

    var ddl = document.getElementById("expense_class_id");
    var selectedOption = ddl.options[ddl.selectedIndex];
    var expen_class_id = selectedOption.getAttribute("id");

    var expense_class = document.getElementById("expense_class");

    for(var i = 1; i < expense_class_list.length; i++) {
        var obj = expense_class_list[i];
        if (obj._id == expen_class_id){
            expense_class.value = obj.name;
            document.getElementById("expense_class").readOnly = true;
            document.getElementById('expense_type_id').style.display = "block";
        }
    }
    var obj = expense_class_list[0];
        if (obj._id == expen_class_id){
            expense_class.value = "";
            document.getElementById("expense_class").readOnly = false;
        }
}

function setExpenseTypeDetails(expense_type_list_10){

    var ddl = document.getElementById("expense_type_id");
    var selectedOption = ddl.options[ddl.selectedIndex];
    var expen_type_id = selectedOption.getAttribute("id");

    var expense_type = document.getElementById("expense_type");

    for(var i = 1; i < expense_type_list_10.length; i++) {
        var obj = expense_type_list_10[i];
        if (obj._id == expen_type_id){
            expense_type.value = obj.name;
            document.getElementById("expense_type").readOnly = true;
        }
    }
    var obj = expense_type_list_10[0];
        if (obj._id == expen_type_id){
            expense_type.value = "";
            document.getElementById("expense_type").readOnly = false;
        }
}
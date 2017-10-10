
    //wtf flask
    var key_value = [];
    function string_to_array(x)
    {


        var temp_id = "";
        var temp_number = "";
        var write_to =0;
        //temp_id = x;
        //temp_number = x;
        //
        for (var i = 0; i<x.length; i++)
        {
            if (x[i] =='/')
            {
                //key_value.push(["t","s"]);
                if (temp_id != "" && temp_number != "")
                {
                    var temp_key_value = [temp_id,temp_number];
                    key_value.push([temp_id,temp_number]);
                  // key_value.push(["t","s"]);
                }
                write_to = 0;
                temp_id = "";
                temp_number = "";
            }
            else if (x[i] == '.')
            {
               // alert(x[i]);
                write_to = 1;
                 //alert("wawe");


            }
            else
            {
                // alert("wele");
                if (write_to ==0)
                {
                    temp_id = temp_id.concat(x[i]);
                }
                else if (write_to ==1)
                {
                    temp_number = temp_number.concat(x[i]);
                }
            }
            //alert(x[i]);
        }
    }

    function create_row()
    {
        var table = document.getElementById("buy_table");
        for (var i = 0; i<key_value.length; i++)
        {
                 var total_rows = document.getElementById("buy_table").rows.length;
                var row = table.insertRow(total_rows);
                var cell0 = row.insertCell(0);
                var cell1 = row.insertCell(1);
                var cell2 = row.insertCell(2);
                cell0.innerHTML = key_value[i][0];
                cell1.innerHTML = key_value[i][1];
                cell2.innerHTML = "PlaySubtotal";
        }

    }

    function display()
    {
       //var form = new FormData(document.querySelector('tickets'))
        //alert("{{tickets}}");
        var x = document.cookie;
        string_to_array(x);
        create_row();
        //alert(key_value.length);
        //document.getElementById("total_cost").innerHTML = tickets;
    }
    display();

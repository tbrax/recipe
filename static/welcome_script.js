                class Play
                {
                    constructor(a,b,c,d,e,f,g)
                    {
                        this.play_id = a;
                        this.play_name = b;
                        this.play_description = c;
                        this.play_time = d;
                        this.play_location = e;
                        this.play_price = f;
                        this.play_seats = g;
                    }
                }
                var p0 = new Play("Oz_id","The Wizard of Oz","Dorthy goes to a strange land");

                var total_play_list = [p0];
                var current_purchases = [0,
                                         0,
                                         0,
                                         0];
                var play_id =["Oz_id",
                              "Mary_id",
                              "Shrek_id",
                              "Pan_id"];

                var play_name = ["The Wizard of Oz",
                                 "Mary Poppins",
                                 "Shrek",
                                 "Peter Pan"];
                var play_description = ["Dorthy goes to a strange land",
                                        "A magical musical",
                                        "A fun new take on the hit movie",
                                        "A boy teaches kids how to fly"];
                var play_time = ["Wednesday February 15 at 7:00 PM",
                                 "Wednesday February 15 at 8:00 PM",
                                 "Wednesday February 15 at 9:00 PM",
                                 "Wednesday February 15 at 10:00 PM"];
                var play_location = ["UAF Theatre",
                                     "UAF Theatre",
                                     "UAF Theatre",
                                     "UAF Theatre"];
                var play_price = [10,
                                  10,
                                  10,
                                  10];



            for (i = 0; i < current_purchases.length; i++)
            {
                add_show(i);
            }


            function create_key_value()
            {
                pass_string = "";
                   for (var r = 0; r<current_purchases.length; r++)
                {
                    if (current_purchases[r] >0)
                    {
                        pass_string+= play_id[r] + "." + current_purchases[r] + "/";
                    }

                }

                document.cookie = pass_string;
                //document.cookie = "information";

            }
             function submit_price()
            {
                //create_key_value();
                document.getElementById("play_value").value = "This is the String that we want";
                console.log(document.getElementById("play_value").value);
                //document.getElementById("play_num_submit").submit();

                return true;

            }

            function update_price()
            {

                var table = document.getElementById("buy_table");
                var total = 0;
                for (var r = 0, n = current_purchases.length; r < n; r++)
                {
                        total += current_purchases[r]*play_price[r];
                        str = "$";
                        str += (current_purchases[r]*play_price[r]).toFixed(2);
                        table.rows[r+1].cells[4].innerHTML = str;
                        //alert(table.rows[r+1].cells[4].innerHTML);
                }
                str2 = "$";
                str2+=total.toFixed(2);
                document.getElementById("total_cost").innerHTML = str2;

            }
            function change_purchase(play, amt)
            {

                if (amt >= 0) {
                current_purchases[play] = amt;
                } else {
                    current_purchases[play] = 0;
                }
                update_price();
                //alert("blabla");

            }

            function add_show(x)
            {

               var view_button = document.createElement("input");
               view_button.type = "button";
               view_button.value = "View";
               view_button.name = "view_ele";
               view_button.onclick = function()
               {
                    display_result(x)
               };

               var add_field= document.createElement("input");
               add_field.type = "number";
               add_field.min = 0;
               add_field.value = 0;
               add_field.name = "add_ele";
               add_field.onchange = function()
               {

                   change_purchase(x, add_field.value);
               };





                var total_rows = document.getElementById("buy_table").rows.length;
                //var x = document.getElementById("my_select").value;
                var table = document.getElementById("buy_table");

                var row = table.insertRow(total_rows);
                var cell0 = row.insertCell(0);
                var cell1 = row.insertCell(1);
                var cell2 = row.insertCell(2);
                var cell3 = row.insertCell(3);
                var cell4 = row.insertCell(4);
                cell0.innerHTML = play_name[x];
                cell1.innerHTML = play_time[x];
                cell2.appendChild(view_button);
                //cell3.innerHTML = current_purchases[x];
                cell3.appendChild(add_field);
                cell4.innerHTML = "$0.00";
            }

            function display_result(x)
            {

                //var x = document.getElementById("my_select").value;
                document.getElementById("Name").innerHTML = play_name[x];
                document.getElementById("Description").innerHTML = play_description[x];
                document.getElementById("Time").innerHTML = play_time[x];
                document.getElementById("Location").innerHTML = play_location[x];
                var str = "$";
                str += play_price[x].toFixed(2);
                document.getElementById("Price").innerHTML = str;
            }

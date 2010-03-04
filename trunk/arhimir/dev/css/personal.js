$(function() {
			$("button[rel]").overlay();
		});
        $("#passdiv").hide();
        $("#infodiv").hide();
        $("#emaildiv").hide();
        function showHide(formelem, infoelem,  text)
        {
            if (infoelem.text() == text)
            {
                infoelem.fadeOut(200);
                infoelem.fadeIn(200);
            }
            else
                infoelem.fadeIn(800);
            infoelem.html("<font color=Red>"+text+"</font>");
            formelem.fadeOut(200);
            formelem.fadeIn(200);
        }
        checkpwd = true;
        function checkForm(form)
        {
            noerror = true;
            tempcheck = checkpwd;
            if(form.password)
            if(!checkpwd && (form.password.value != ""))
            {
            	checkpwd = true
            }
			if(form.password)
            if((checkpwd) && ((form.password.value != form.pascheck.value) || (form.password.value=='')))
            {
                showHide($("#password"), $("#passdiv"), "Пароль введен неверно");
                $("#passwordcheck").fadeOut(200);
                $("#passwordcheck").fadeIn(200);
                noerror = false;
            }
            if(form.phone)
            if(!true)
            {
                showHide($("#phone"), $("#phonediv"), "Телефон введен неверно");
                noerror = false;
            }
            if(form.name)
            if(form.name.value == '')
            {
                showHide($("#name"), $("#namediv"), "Имя введено неверно");
                noerror = false;
            }
            if(form.surname)
            if(form.surname.value == '')
            {
                showHide($("#surname"), $("#surnamediv"), "Фамилия введена неверно");
                noerror = false;
            }
            if(form.email)
            if(form.email.value == '' || !emailCheck(form.email.value) || $("#emaildiv").text()=="Пользователь с таким адресом уже зарегистрирован" || $("#emaildiv").text()=="Почта введена неверно")
            {
                showHide($("#email"), $("#emaildiv"), "Почта введена неверно");
                noerror = false;
            }
            if(form.login)
            if($("#infodiv").text()!='Логин '+form.login.value+' свободен')
            {
                showHide($("#login"), $("#infodiv"), "Логин введен неверно");
                noerror = false;
            }
            checkpwd = tempcheck;
            return noerror;
        }
        function emailCheck(str) {
            var at="@"
            var dot="."
            var lat=str.indexOf(at)
            var lstr=str.length
            if (str.indexOf(at)==-1 || str.indexOf(at)==-1 || str.indexOf(at)==0 || str.indexOf(at)==lstr
                || str.indexOf(dot)==-1 || str.indexOf(dot)==0 || str.indexOf(dot)==lstr || str.indexOf(at,(lat+1))!=-1
                || str.indexOf(at,(lat+1))!=-1 || str.indexOf(dot,(lat+2))==-1 || str.indexOf(" ")!=-1) return false
            else return true
        }
        function showUserName() {
            if($("#login").attr("value")=="")
            {
                $("#infodiv").fadeOut(400);
            }
            else
            {
                $("#infodiv").fadeIn(1000);
            }
        }
        var usName = "";
        var usMail = "";
        var emailLoad = false;
        function loadEmail() {
        	if($("#email").attr("value")=="")
				$("#emaildiv").fadeOut(400);
			else
			{
	        	if(emailCheck($("#email").attr("value"))) {
	        		$("#emaildiv").html("<fo" + "nt color = Green>Почта введена верно</fo" + "nt>");
	        		$("#emaildiv").fadeIn(1000);
	        	}
	        	else {
	        		$("#emaildiv").html("<fo" + "nt color = Red>Почта введена неверно</fo" + "nt>");
	                $("#emaildiv").fadeIn(1000);
	        	}
        	}
        }
        function loadUserName() {
            if ($("#login").attr("value") != usName)
            {
                $("#infodiv").load("/checklog/", {"username" : $("#login").attr("value")});
                showUserName();
            }
            usName = $("#login").attr("value");
            setTimeout('loadUserName();', 3000);
        }
        $(document).ready(function() {
            $("#login").keyup(function() {
                if($("#login").attr("value")=="")
                    $("#infodiv").fadeOut(400);
            });
            $("#name").keyup(function() {
                if($("#namediv").text() == "Имя введено неверно" && $("#name").attr("value") != "")
                    $("#namediv").fadeOut(400);
            });
            $("#surname").keyup(function() {
                if($("#surnamediv").text() == "Фамилия введена неверно" && $("#surname").attr("value") != "")
                    $("#surnamediv").fadeOut(400);
            });
            $("#passwordcheck").keyup(function() {
                if($("#passwordcheck").attr("value")=="")
                {
                    $("#passdiv").fadeOut(400);
                }
                else
                {
                	var expr = new RegExp('\\w', 'g');
                	if (!expr.test($("#passwordcheck").attr("value")) || !expr.test($("#password").attr("value")))
                	{
                		$("#passdiv").html("<fo" + "nt color = Red>Пароль должен содержать только символы, букв латинского алфавита и цифры.</fo" + "nt>");
                	}
                	else
                	{
	                    if($("#passwordcheck").attr("value") != $("#password").attr("value"))
	                    {
	                        $("#passdiv").html("<fo" + "nt color = Red>Пароли не совпадают</fo" + "nt>");
	                        $("#passdiv").fadeIn(1000);
	                    }
	                    else
	                    {
	                        $("#passdiv").html("<fo" + "nt color = Green>Пароли введены верно</fo" + "nt>");
	                        $("#passdiv").fadeIn(1000);
	                    }
	                }
                }
            });
            $("#email").keyup(function() {
                loadEmail();
            });
            
        });
        function search(t)
	    {
	    	$("#tag_search_val").val(t);
	    	$("#tag_search").submit();
	    }
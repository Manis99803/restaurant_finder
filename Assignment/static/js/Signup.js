$('#user_signup').on('click', function(e) {
          var firstName = $("#firstName").val()
          var lastName = $("#lastName").val()
          var emailId = $("#email-Id").val()
          var password = $("#password").val()
          var userObject = {}
          userObject["firstName"] = firstName
          userObject["lastName"] = lastName
          userObject["emailId"] = emailId
          userObject["password"] = password
          if (firstName != '') {
            if (lastName != '') {
              if (isValidEmailAddress(emailId)) {
                if (password != '') {
                  $.ajax({
                  url : 'http://localhost:5000/user_signup',
                  dataType : "json",
                  type : "POST",
                  contentType: "application/json",
                  xhrFields: {withCredentials: false},
                  crossDomain: true,
                  data: JSON.stringify(userObject),
                  success: function(data) {
                      window.location.href = 'http://localhost:5000/login'
                  },
                  error: function(jqXHR, textStatus, errorThrown) {
                    statusCode = (jqXHR.status);
                    raiseError("The given email id is already registered with us")
                  }
            });
                }
                else {
                  raiseError("Please Provide Proper Credentials")
                }
              }
              else {
                raiseError("Please Provide Proper Credentials")
              }
            }
            else {
              raiseError("Please Provide Proper Credentials")
            }
          } 
          else {
            raiseError("Please Provide Proper Credentials")
          }  

      });

      function raiseError(errorMessage) {
          console.log("raise Error called")
          $("#outputFeedBack").css("display","block")
          $("#outputFeedBack").css("color","#FFFFFF")
          $("#outputFeedBack").html(errorMessage)
      }

      function isValidEmailAddress(emailAddress) {
          var pattern = new RegExp(/^(("[\w-+\s]+")|([\w-+]+(?:\.[\w-+]+)*)|("[\w-+\s]+")([\w-+]+(?:\.[\w-+]+)*))(@((?:[\w-+]+\.)*\w[\w-+]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$)|(@\[?((25[0-5]\.|2[0-4][\d]\.|1[\d]{2}\.|[\d]{1,2}\.))((25[0-5]|2[0-4][\d]|1[\d]{2}|[\d]{1,2})\.){2}(25[0-5]|2[0-4][\d]|1[\d]{2}|[\d]{1,2})\]?$)/i);
          return pattern.test(emailAddress);
      };
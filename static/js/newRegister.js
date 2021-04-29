$("#medium-indicator").dxLoadIndicator({
        height: 40,
        width: 40
});

$.ajaxSetup({async: false});

var Interest;
var Skills;

$.getJSON("https://vinda-beta.herokuapp.com/members/getInterest/", function(json){Interest = json;});
$.getJSON("https://vinda-beta.herokuapp.com/members/getSkills/", function(json){Skills = json;});

$.ajaxSetup({ async: true });



$(function() {
    var sendRequestForEmail = function(value) {
        var d = $.Deferred();
        setTimeout(function() {

            var form = new FormData();
            form.append("email", value);

            var settings = {
              "url": "verifymail",
              "method": "POST",
              "timeout": 0,
              "processData": false,
              "headers": {
                "X-CSRFToken": csrftoken,
                "Access-Control-Allow-Origin": "http://vinda-beta.herokuapp.com,https://vinda-beta.herokuapp.com",
                "Access-Control-Allow-Headers" : "Accept,Content-Type,X-Requested-With,x-api-key",
              },
              "mimeType": "multipart/form-data",
              "contentType": false,
              "data": form
            };

            $.ajax(settings).done(function (response) {
                var JSONresponse = JSON.parse(response)
                var existe = (JSONresponse.existe === 'true');
                var institucion = (JSONresponse.institucion === 'true');
                d.resolve(!existe);
            });
        }, 1000);
        return d.promise();
    }

    var sendRequestForUsername = function(value) {
        var d = $.Deferred();
        setTimeout(function() {

            var form = new FormData();
            form.append("username", value);

            var settings = {
              "url": "verifyusername",
              "method": "POST",
              "timeout": 0,
              "processData": false,
              "headers": {
                "X-CSRFToken": csrftoken,
                "Access-Control-Allow-Origin": "http://vinda-beta.herokuapp.com,https://vinda-beta.herokuapp.com",
                "Access-Control-Allow-Headers" : "Accept,Content-Type,X-Requested-With,x-api-key",
              },
              "mimeType": "multipart/form-data",
              "contentType": false,
              "data": form
            };

            $.ajax(settings).done(function (response) {
                var JSONresponse = JSON.parse(response)
                var existe = (JSONresponse.existe === 'true');
                d.resolve(!existe);
            });
        }, 1000);
        return d.promise();
    }

    var formWidget = $("#form").dxForm({
        items: [{
            itemType: "group",
            cssClass: "first-group",
            colCount: 4,
            items: [
                {
                    itemType: "group",
                    items: [{
                        template: "<div class='form-avatar'></div>"
                    },{
                        dataField: "image",
                        label: {
                            visible:false,
                        },
                        editorType: "dxFileUploader",
                        editorOptions: {
                            selectButtonText: "Seleccionar foto",
                            labelText:"o arrástrala hasta aquí",
                            accept: "image/*",
                            uploadMode: "useForm",
                            maxFileSize: 100000,
                            showFileList: false,
                            onValueChanged: function(e){
                                if (e.value.length) {
                                    console.log(e.value[0]);
                                    changeImage(e.value[0]);
                                }
                            }
                        },
                        validationRules: [{
                            type: "required",
                            message: "Usted deberá de subir una foto de perfil para crearse una cuenta"
                        }]
                    }]
                },{
                itemType: "group",
                colSpan: 3,
                items: [{
                    dataField: "username",
                    label: {
                        text:"Usuario"
                    },
                    validationRules: [{
                      type: "required",
                      message: "Usted deberá de crearse un usuario"
                    }, {
                        type: "async",
                        message: "El usuario ingresado ya se encuentra registrado",
                        validationCallback: function(params) {
                            return sendRequestForUsername(params.value);
                        }
                    },{
                        type: 'pattern',
                        pattern: '(^[a-zA-Z0-9]*$)',
                        message: 'Solo podrás utilizar letras y números.'

                    }]

                }, {
                    dataField: "name",
                    label: {
                        text:"Nombre Completo"
                    },
                    validationRules: [{
                      type: "required",
                      message: "Usted deberá de ingresar su nombre completo."
                    }]

                }, {
                    dataField: "email",
                    label: {
                        text:"Correo Electrónico"
                    },
                    validationRules: [{
                        type: "required",
                        message: "Usted deberá de ingresar su correo electrónico."
                      }, {
                        type: "email",
                        message: "El correo es inválido"
                      }, {
                        type: 'pattern',
                        pattern: '^[\\w-\\.]+@([\\w-]+\\.)+edu(\\.[\\w-]{2,4})?$',
                        message: 'El correo no es institucional'
                      }, {
                        type: "async",
                        message: "El correo ingresado ya se encuentra registrado",
                        validationCallback: function(params) {
                            return sendRequestForEmail(params.value);
                        }
                    }]
                },{
                    dataField: "password",
                    label: {
                        text:"Contraseña"
                    },
                    editorOptions: {
                        mode: "password"
                    },
                    validationRules: [{
                        type: "required",
                        message: "Contraseña requerida"
                    },{
                        type: 'pattern',
                        pattern: '(?=.*[0-9])',
                        message: 'Su contraseña no es segura. Incluir, por lo menos, un número.'
                    },{
                        type: 'pattern',
                        pattern: '(?=.*[a-z])(?=.*[A-Z])',
                        message: 'Su contraseña no es segura. Incluir, por lo menos, una letra mayúscula y minúscula.'
                    },{
                        type: 'pattern',
                        pattern: '.{8,32}',
                        message: 'Su contraseña no es segura. La longitud debe de ser mayor a 8 caracteres.'
                    }
                    ]
                },{
                label: {
                    text: "Confirmar la Contraseña"
                },
                editorType: "dxTextBox",
                editorOptions: {
                    mode: "password"
                },
                validationRules: [{
                    type: "required",
                    message: "Es necesario confirmar su contraseña"
                }, {
                    type: "compare",
                    message: "'Contraseña' y 'Confirmar la Contraseña' no son iguales",
                    comparisonTarget: function() {
                        return formWidget.option("formData").password;
                    }
                }]
              }]
            }]
        }, {
            itemType: "group",
            cssClass: "second-group",
            colCount: 2,
            items: [{
                itemType: "group",
                items: [{
                    dataField: "summary",
                    label: {
                        text: "Soy un estudiante"
                    },
                    editorType: "dxTextBox",
                    editorOptions: {
                        placeholder: "Soy un estudiante de BioIngeniería, apasionado por los nuevos materiales."
                    },
                    validationRules: [{
                        type: "stringLength",
                        max: 135,
                        message: "Se más breve.",
                        ignoreEmptyValue: true
                    }]
                }]
                },{
                itemType: "group",
                items: [{
                    dataField: "phone",
                    label: {
                        text: "Número Celular"
                    },
                    editorOptions: {
                        mask: "+51 000-000-000"
                    }
                }]
            }, {
                colSpan: 2,
                dataField: "linkin",
                label: {
                  text: "Perfil de Linkedin"
                },
                editorType: "dxTextBox",
                editorOptions: {
                    mode: "Url",
                    placeholder: "https://www.linkedin.com/in/tuusuario",
                },validationRules: [{
                    type: 'pattern',
                    pattern: '\(?:(?:https?|ftp|file):\/\/|www\.|ftp\.)(?:\([-A-Z0-9+&@#\/%=~_|$?!:,.]*\)|[-A-Z0-9+&@#\/%=~_|$?!:,.])*(?:\([-A-Z0-9+&@#\/%=~_|$?!:,.]*\)|[A-Z0-9+&@#\/%=~_|$])',
                    message: 'Dirección URL inválida.'
                }]
            }, {
                colSpan: 2,
                dataField: "description",
                label: {
                  text: "Me apasiona"
                },
                editorType: "dxTextArea",
                editorOptions: {
                    height: 140,
                    spellcheck:true,
                }
            }, {
                colSpan: 2,
                dataField: "skill",
                label: {
                  text: "Skills"
                },
                editorType: "dxTagBox",
                editorOptions: {
                    dataSource: new DevExpress.data.ArrayStore({
                        data: Skills,
                        key: "slug"
                    }),
                    displayExpr: "name",
                    valueExpr: "slug",
                    searchEnabled: true,
                    hideSelectedItems: true,
                    placeholder: "Elegir los skills que te identifiquen...",
                }
            }, {
                colSpan: 2,
                dataField: "interest",
                label: {
                  text: "Interest"
                },
                editorType: "dxTagBox",
                editorOptions: {
                    dataSource: new DevExpress.data.ArrayStore({ 
                        data: Interest,
                        key: "slug"
                    }),
                    displayExpr: "name",
                    valueExpr: "slug",
                    searchEnabled: true,
                    hideSelectedItems: true,
                    placeholder: "Elegir los intereses que te identifiquen...",
                }
            }]
        }, {
            itemType: "button",
            horizontalAlignment: "right",
            buttonOptions: {
                text: "Registrarme",
                type: "success",
                useSubmitBehavior: true
            }
        }]
    }).dxForm("instance");
    $("#medium-indicator").hide();
});


var formData = {
    "password": ""
};


var RenderImagen;

function changeImage(file){
    var reader = new FileReader();
    reader.onloadend = function(){
      document.getElementsByClassName("form-avatar")[0].style.backgroundImage = "url(" + reader.result + ")";
    }
    if(file){ reader.readAsDataURL(file);}
    RenderImagen = reader;
    console.log(RenderImagen);
}

$(document).ready(function() {
    document.getElementById('file-input').addEventListener('change', readURL, true);
    function readURL(){
       var file = document.getElementById("file-input").files[0];
       var reader = new FileReader();
       reader.onloadend = function(){
          document.getElementsByClassName("form-avatar")[0].style.backgroundImage = "url(" + reader.result + ")";
       }
       if(file){ reader.readAsDataURL(file);}
       RenderImagen = reader;
       console.log(RenderImagen);
    }

    $(".upload-button").on('click', function() {
       $(".file-upload").click();
    });

});


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');


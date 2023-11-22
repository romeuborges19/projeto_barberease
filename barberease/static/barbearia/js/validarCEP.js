$(document).ready(function() {
    console.log("anan0");
    $('#id_cep').blur(function (){
        console.log("anjakdja");
        var valor_cep = $('#id_cep').val();
        valor_cep = valor_cep.replace(/[^0-9]/g, '');
        console.log(valor_cep)
        if(valor_cep.length == 8){
            console.log("entrou");
            valor_cep = parseInt(valor_cep, 10);
            verificarCep(valor_cep);
        }
    })

function verificarCep(data){
    console.log(data)
    var link = "https://viacep.com.br/ws/"+data+"/json/";
    $.ajax({
        url: link,
        data: 'GET',
        dataType: 'json',
    
        success: function(data) {
 
            if (data.erro){
                // tratar erro aqui
                // $("div.cadastro").html(' <div class="alert alert-danger" role="alert" A simple danger alert—check it out!</div>');
            }else{
                $('#id_endereco').val(data.logradouro);
                $('#id_setor').val(data.bairro);
                $('#id_cidade').val(data.localidade);
                $('#id_estado').val(data.uf);
            }
           
        },
        error: function(xhr, errmsg, err) {
            console.log("deu erro");
        }
    });
    
}

});
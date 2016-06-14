/**
 * Created by lalbuquerque on 20/05/2016.
 */

$(document).ready(function() {
    var questFinish = false;
    var respostas = [];
    var is_first = true;
    var counter = 0;
    var questId = $("#quest-" + counter);

    var type_pot = null;
    var val_pot = 0;
    var val_prov = 0;

    function enableRadio(){
        if(!getValue() && !type_pot){
            $("input").attr('disabled', true);
        } else {
            $("input").attr('disabled', false);
        }
    }

    function getValue(){
        questIdDB = $("#quest-"+counter+" input.questId").val();
        val = $("input[name='respQuadro-"+questIdDB+"']:checked").val();
        return val ;
    }

    function selectRadio(value){
        if(value>0){
            $("#resp-"+value).prop('checked', true);
        } else {
            $('input').removeAttr('checked');
        }
    }

    function writeRespDB(){
        impacto = $("#impactoId").val();
        str_json = {'impacto': impacto, 'respostas': respostas};

        xmlhttp = new XMLHttpRequest();   // new HttpRequest instance
        xmlhttp.open("POST", "/impacto/quadro/");
        xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xmlhttp.send(JSON.stringify(str_json));
        window.location.href = "/impacto/quadro/gabarito/"+impacto+"/";
    }

    function saveResp(value_prov, value_pot){
        resp = {'provavel': value_prov, 'potencial': value_pot};
        respostas.push(resp);
    }

    function finishQuest(){
        questFinish = true;
        $(".PPSelect").hide();
        $("#toggle_questao").hide();
        console.log(respostas);
    }

    function resetPP(){
        type_pot = null;
        val_pot = 0;
        val_prov = 0;
        $("#prov-tr").removeClass("PPSelected");
        $("#pot-tr").removeClass("PPSelected");
        $("#pot-value").text("Nenhum Selecionado");
        $("#prov-value").text("Nenhum Selecionado");
    }
    function nextQuest(){
        questId.hide("fast");
        counter++;
        questId = $("#quest-" + counter);
        resetPP();
        enableRadio();
        questId.show("fast");
        if($("#quest-" + (parseInt(counter)+1)).length == 0) {
            $("#toggle_questao").text("Finalizar Questionário");
        }
        if(questId.length == 0){ finishQuest(); writeRespDB(); }
    }

    function processQuest(){
        if (is_first){
            $(".PPSelect").show();
            $("#toggle_questao").text("Próxima Questão");
            nextQuest();
            is_first = false;
        } else if (!questFinish && val_pot > 0 && val_prov > 0) {
            saveResp(val_prov, val_pot);
            nextQuest();
        } else {
            alert("Você precisa responder as perguntas.");
        }
    }

    function processPot(){
        $("#prov-tr").removeClass("PPSelected");
        $("#pot-tr").addClass("PPSelected");
        type_pot = 1;
        selectRadio(val_pot);
        enableRadio();

    }

    function processProv(){
        $("#pot-tr").removeClass("PPSelected");
        $("#prov-tr").addClass("PPSelected");
        type_pot = 2;
        selectRadio(val_prov);
        enableRadio();
    }

    $("#toggle_questao").click((function(){
        return function() { processQuest(); }
    })());

    $("#pot-tr").click((function(){
        return function() { processPot(); }
    })());

    $("#prov-tr").click((function(){
        return function() { processProv(); }
    })());

    $("input").change(function() {
        valueRadio = getValue();
        if(type_pot == 1){
            val_pot = valueRadio;
            $("#pot-value").text($("#respLabel-"+val_pot+"").text());
        } else {
            val_prov = valueRadio;
            $("#prov-value").text($("#respLabel-"+val_prov+"").text());
        }
    });
});
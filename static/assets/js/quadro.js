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

    function getValue(){
        var questIdDB = $("#quest-"+counter+" input.questId").val();
        var valueSelect = $("input[name='respQuadro-"+questIdDB+"']:checked").val();
        return valueSelect;
    }

    function saveResp(value){
        respostas.push(parseInt(value));
    }

    function finishQuest(){
        questFinish = true;
        $(".PPSelect").hide();
        $("#toggle_questao").hide();
        console.log(respostas);
    }

    function nextQuest(){
        questId.hide("fast");
        counter++;
        questId = $("#quest-" + counter);
        questId.show("fast");
        if($("#quest-" + (parseInt(counter)+1)).length == 0) {
            $("#toggle_questao").text("Finalizar Questionário");
        }
        if(questId.length == 0){ finishQuest(); }
    }

    function processQuest(valueSelect){
        if (is_first){
            $(".PPSelect").show();
            $("#toggle_questao").text("Próxima Questão");
            nextQuest();
            is_first = false;
        } else if (!questFinish && valueSelect) {
            saveResp(valueSelect);
            nextQuest();
        } else {
            alert("Você precisa responder as perguntas.");
        }
    }

    function processPot(valueSelect){
        if (!valueSelect){ valueSelect = 0; }
        val_pot = valueSelect;
        $("#prov-tr").removeClass("PPSelected");
        $("#pot-tr").toggleClass("PPSelected");
        console.log("Potencial:"+val_pot);
    }

    function processProv(valueSelect){
        if (!valueSelect){ valueSelect = 0; }
        val_prov = valueSelect;
        $("#pot-tr").removeClass("PPSelected");
        $("#prov-tr").toggleClass("PPSelected");
        console.log("Provável:"+val_prov);

    }

    $("#toggle_questao").click((function(){
        return function() { processQuest(getValue()); }
    })());

    $("#pot-tr").click((function(){
        return function() { processPot(getValue()); }
    })());

    $("#prov-tr").click((function(){
        return function() { processProv(getValue()); }
    })());
});
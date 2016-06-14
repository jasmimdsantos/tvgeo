$(".form-reset").submit(function(e) {
    e.preventDefault();

    $(".btn-send-reset").data("original", $(".btn-send-reset").text());
    $(".btn-send-reset").text("Aguarde...").attr("disabled", true);

    $.post("/reset/", function(obj) {
        bootbox.alert("Você receberá um email com os detalhes para criar uma nova senha!");
        $(".btn-send-reset").text($(".btn-send-reset").data("original")).attr("disabled", false);
    }, 'JSON').error(function() {
        bootbox.alert("Falha ao tentar solicitar nova senha, tente novamente mais tarde!");
        $(".btn-send-reset").text($(".btn-send-reset").data("original")).attr("disabled", false);
    });
});
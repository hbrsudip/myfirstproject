$(document).ready(function() {
    $("#postfix").change(function() {
        let postfix = $(this).val();
        $.post("/process_postfix", JSON.stringify({ postfix }), function(response) {
            if (response.prompt) {
                let customPostfix = prompt("Enter custom postfix:");
                if (customPostfix) {
                    $("#output").append(`<p>Selected Postfix: ${customPostfix}</p>`);
                }
            } else {
                $("#output").append(`<p>${response.message}</p>`);
            }
        }, "json");
    });

    $("#variant").change(function() {
        let variant = $(this).val();
        $.post("/process_variant", JSON.stringify({ variant }), function(response) {
            if (response.prompt) {
                let customVariant = prompt("Enter custom variant path:");
                if (customVariant) {
                    $("#output").append(`<p>Selected Variant Path: ${customVariant}</p>`);
                }
            } else {
                $("#output").append(`<p>${response.message}</p>`);
            }
        }, "json");
    });

    $("#create-sn-sheet").click(function() {
        let postfix = $("#postfix").val();
        let variant = $("#variant").val();
        $.post("/create_sn_sheet", JSON.stringify({ postfix, variant }), function(response) {
            $("#output").append(`<p>${response.message}</p>`);
        }, "json");
    });

    $("#create-mapping-sheets").click(function() {
        let selectedVariants = $("#variant-list").val();
        $.post("/create_mapping_sheet", JSON.stringify({ selected_variants: selectedVariants }), function(response) {
            $("#output").append(`<p>${response.message}</p>`);
        }, "json");
    });
});

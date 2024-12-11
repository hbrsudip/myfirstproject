$(document).ready(function() {
    // Handle Postfix Selection
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

    // Handle Variant Selection
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

    // Create SN Sheet
    $(document).ready(function() {
    $("#create-sn-sheet").click(function() {
        // Get user inputs
        let postfix = $("#postfix").val();
        let variant = $("#variant").val();

        // Check if both inputs are provided
        if (!postfix || !variant) {
            alert("Please select both a postfix and a variant.");
            return;
        }

        // Send data to the Flask backend
        $.post("/create_sn_sheet", 
            JSON.stringify({ postfix: postfix, variant: variant }), 
            function(response) {
                $("#output").append(`<p>${response.message}</p>`);
            }, 
            "json"
        ).fail(function() {
            alert("Error: Could not create SN sheet. Please try again.");
        });
    });
});


    // Create Mapping Sheets
    $("#create-mapping-sheets").click(function() {
        let selectedVariants = $("#variant-list").val();
        $.post("/create_mapping_sheet", JSON.stringify({ selected_variants: selectedVariants }), function(response) {
            $("#output").append(`<p>${response.message}</p>`);
        }, "json");
    });
});

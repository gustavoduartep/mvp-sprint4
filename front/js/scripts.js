$(document).ready(function () {
  $(".numeric").inputmask({
    alias: "numeric",
    allowMinus: false,
    digits: 4,
    rightAlign: false,
    max: 99.9999,
  });

  $(".avaliacao").inputmask({
    mask: "9",
    placeholder: "0",
    min: 0,
    max: 10,
  });

  $("#adicionarVinho").click(function (e) {
    e.preventDefault();
    var formData = new FormData();

    formData.append("fixed_acidity", $("#fixed_acidity").val());
    formData.append("volatile_acidity", $("#volatile_acidity").val());
    formData.append("citric_acid", $("#citric_acid").val());
    formData.append("residual_sugar", $("#residual_sugar").val());
    formData.append("chlorides", $("#chlorides").val());
    formData.append("free_sulfur_dioxide", $("#free_sulfur_dioxide").val());
    formData.append("total_sulfur_dioxide", $("#total_sulfur_dioxide").val());
    formData.append("density", $("#density").val());
    formData.append("ph", $("#ph").val());
    formData.append("sulphates", $("#sulphates").val());
    formData.append("alcohol", $("#alcohol").val());

    console.log("Vinho Data:", formData);

    $.ajax({
      type: "POST",
      url: "http://127.0.0.1:5000/vinho",
      data: formData,
      processData: false, // Evita que o jQuery processe os dados, pois o FormData já cuida disso
      contentType: false, // Evita que o jQuery defina automaticamente o cabeçalho 'Content-Type'
      success: function (response) {
        //$("#vinhoForm")[0].reset();
        carregaTabela();
        exibirAlerta(
          "success",
          "Sucesso!",
          "O vinho foi adicionado na pesquisa.",
          3000
        );
      },
      error: function (error) {
        console.error("Erro ao enviar dados:", error);
      },
    });
  });

  carregaTabela();
});

function deletarVinho(idVinho) {
  Swal.fire({
    title: "Remover o dado?",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#CCC",
    confirmButtonText: "Sim",
    confirmButtonColor: "#721c24",
    background: "#FFF",
    color: "#721c24",
    cancelButtonText: "Cancelar",
  }).then((result) => {
    if (result.isConfirmed) {
      $.ajax({
        url: `http://127.0.0.1:5000/vinho?id=${idVinho}`,
        method: "DELETE",
        success: function () {
          carregaTabela();

          Swal.fire({
            title: "Removido!",
            text: "Vinho removido da base de dados.",
            icon: "success",
            confirmButtonText: "Ok",
            color: "#721c24",
            confirmButtonColor: "#721c24",
            background: "#FFF",
            timer: 3000,
          });
        },
      });
    }
  });
}

// Modal para exibir o resultado dos eventos
function exibirAlerta(status, titulo, texto, tempo) {
  Swal.fire({
    position: "center",
    title: titulo,
    text: texto,
    icon: status,
    color: "#fff",
    showConfirmButton: false,
    background: "#212529",
    timer: tempo,
  });
}

function carregaTabela() {
  $.ajax({
    type: "GET",
    url: "http://127.0.0.1:5000/vinhos",
    dataType: "json",
    success: function (data) {
      $("#vinhoTable tbody").empty();

      $.each(data.vinhos, function (index, vinho) {
        var qualidade_vinho =
          vinho.quality == 1
            ? "<span class='quality-indicator '><i class='fa fa-caret-up above-average'></i> Acima da média</span>"
            : "<span class='quality-indicator'><i class='fa fa-caret-down below-average'></i> Abaixo da média</span>";
        console.log(`Qualidade do vinho: ${vinho.quality}`);
        console.log(`Tratamento: ${vinho.quality}`);

        var row = "<tr>";
        row += "<td>" + vinho.id + "</td>";
        row += "<td>" + vinho.volatile_acidity + "</td>";
        row += "<td>" + vinho.citric_acid + "</td>";
        row += "<td>" + vinho.residual_sugar + "</td>";
        row += "<td>" + vinho.chlorides + "</td>";
        row += "<td>" + vinho.free_sulfur_dioxide + "</td>";
        row += "<td>" + vinho.total_sulfur_dioxide + "</td>";
        row += "<td>" + vinho.density + "</td>";
        row += "<td>" + vinho.ph + "</td>";
        row += "<td>" + vinho.sulphates + "</td>";
        row += "<td>" + vinho.alcohol + "</td>";
        row += "<td>" + qualidade_vinho + "</td>";
        row +=
          "<td><i class='fa fa-trash deletar-vinho' aria-hidden='true' onclick='deletarVinho(" +
          vinho.id +
          ")'></i></td>";
        row += "</tr>";

        // Adicionar a linha à tabela
        $("#vinhoTable tbody").append(row);
      });
    },
    error: function (error) {
      console.error("Erro ao carregar a tabela:", error);
    },
  });
}

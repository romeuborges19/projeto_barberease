$(document).ready(function(){
	$('.approve-button').click(function() {

		const pedidoId = $(this).data('pedido-id');
		const url = 'agendamento/pedidos/' + {{ pk }} + '/';
		$.ajax({
			url: url, 
			type: 'POST',
			data: { pedido_id: pedidoId},
			success: function(response){
				if (response.error) {
					alert(response.error);
				} else {
					alert(response.message);
					const pedidoAtualizado = $(`[data-pedido-id="$(pedidoId)]"`);
					pedidoAtualizado.find('.aprovado').text(response.aprovado);
				}
			}
		})
	}) 
})

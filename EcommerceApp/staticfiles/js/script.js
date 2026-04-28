console.log("Hi there");

$(".plus-cart").click(function () {
  var id = $(this).attr("pid").toString();
  var quantity = this.parentNode.children[2];

  $.ajax({
    type: "GET",
    url: "/pluscart",
    data: {
      prod_id: id,
    },
    success: function (data) {
      quantity.innerText = data.quantity;
      document.getElementById("amount").innerText = data.amount;
      document.getElementById("totalamount").innerText = data.totalamount;
    },
  });
});

$(".minus-cart").click(function () {
  var id = $(this).attr("pid").toString();
  var quantity = this.parentNode.children[2];

  $.ajax({
    type: "GET",
    url: "/minuscart",
    data: {
      prod_id: id,
    },
    success: function (data) {
      quantity.innerText = data.quantity;
      document.getElementById("amount").innerText = data.amount;
      document.getElementById("totalamount").innerText = data.totalamount;
    },
  });
});

$(".remove-cart").click(function () {
  var id = $(this).attr("pid").toString();
  var el = this;

  $.ajax({
    type: "GET",
    url: "/removeitem",
    data: {
      prod_id: id,
    },
    success: function (data) {
      document.getElementById("amount").innerText = data.amount;
      document.getElementById("totalamount").innerText = data.totalamount;
      el.parentNode.parentNode.parentNode.parentNode.remove();
    },
  });
});

$(".plus-wishlist").click(function () {
  var id = $(this).attr("pid").toString();
  host = window.location.host;

  $.ajax({
    type: "GET",
    url: "/pluswishlist",
    data: {
      prod_id: id,
    },
    success: function (data) {
      // window.location.reload();
      window.location.href = `http://${host}/product-detail/${id}`;
    },
  });
});

$(".minus-wishlist").click(function () {
  var id = $(this).attr("pid").toString();
  host = window.location.host;

  $.ajax({
    type: "GET",
    url: "/minuswishlist",
    data: {
      prod_id: id,
    },
    success: function (data) {
      // window.location.reload();
      window.location.href = `http://${host}/product-detail/${id}`;
    },
  });
});

function makePayment() {
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/make-payment/", true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      console.log(xhr.responseText);
    }
  };
  xhr.send(
    JSON.stringify({
      amount: 2500,
      name: "Test Plan",
      interval: "monthly",
    })
  );
}

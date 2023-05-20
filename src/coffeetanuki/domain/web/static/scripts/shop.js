// Extract shop ID from URL path
const shopId = window.location.pathname.split("/").pop();

// Fetch shop details from the API
fetch(`/api/shops/${shopId}`)
  .then((response) => response.json())
  .then((shop) => {
    const shopDetails = document.getElementById("shop-details");
    shopDetails.innerHTML = `
          <h1 class="text-3xl text-center font-bold mb-8">${shop.name}</h1>
          <p><strong>Address:</strong> ${shop.address}</p>
          <p><strong>Hours of Operation:</strong> ${shop.hours_of_operation}</p>
        `;
  })
  .catch((error) => {
    console.error("Error:", error);
  });

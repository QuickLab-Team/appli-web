document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("search");
    const productList = document.querySelectorAll(".product-item");
    
    searchInput.addEventListener("keyup", function () {
        const searchText = searchInput.value.toLowerCase();
        
        productList.forEach(product => {
            const productName = product.querySelector(".product-name").textContent.toLowerCase();
            
            if (productName.includes(searchText)) {
                product.style.display = "block";
            } else {
                product.style.display = "none";
            }
        });
    });
});

import Dashboard from "views/Dashboard.js";
import ProductDetails from "views/ProductDetails.js"; 

var routes = [
  {
    path: "/dashboard",
    name: "Dashboard",
    icon: "nc-icon nc-bank",
    component: <Dashboard />,
    layout: "/admin",
  },
  {
    path: "/product-details/:id",
    name: "Product Details",
    icon: "nc-icon nc-box",
    component: <ProductDetails/>,
    layout: "/admin",
  },
];
export default routes;

import React from "react";
import { Card, CardBody, CardFooter, Row, Col } from "reactstrap";

const products = [
  { name: "Product 1", image: "path/to/image1.jpg", price: "$150" },
  { name: "Product 2", image: "path/to/image2.jpg", price: "$200" },
  { name: "Product 3", image: "path/to/image3.jpg", price: "$175" },
  { name: "Product 4", image: "path/to/image4.jpg", price: "$225" },
];

function ProductCards() {
  return (
    <div className="content">
      <Row>
        {products.map((product, index) => (
          <Col lg="3" md="6" sm="6" key={index}>
            <Card className="product-card">
              <CardBody className="p-0">
                <img
                  src={product.image}
                  alt={product.name}
                  className="img-fluid"
                />
              </CardBody>
              <CardFooter className="text-center bg-white">
                <strong>{product.price}</strong>
              </CardFooter>
            </Card>
          </Col>
        ))}
      </Row>
    </div>
  );
}

export default ProductCards;
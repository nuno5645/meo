import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { Card, CardBody, CardFooter, Row, Col, Badge } from "reactstrap";

const ProductDetails = () => {
  const { id } = useParams();
  const [product, setProduct] = useState(null);

  useEffect(() => {
    const hostname = window.location.hostname;
    const baseUrl = hostname === 'localhost' ? 'http://localhost' : `http://${hostname}`;
    
    fetch(`${baseUrl}/api/products/${id}/`)
      .then(response => response.json())
      .then(data => setProduct(data))
      .catch(error => console.error('Error fetching data:', error));
  }, [id]);

  if (!product) {
    return <div>Loading...</div>;
  }

  return (
    <div className="content">
      <Row>
        <Col lg="6" className="mb-4">
          <Card className="h-100" style={{ borderRadius: "15px" }}>
            <div className="card-img-top-wrapper" style={{ height: "300px", overflow: "hidden", borderTopLeftRadius: "15px", borderTopRightRadius: "15px" }}>
              <img 
                src={product.image_url} 
                alt={product.name} 
                className="card-img-top"
                style={{ 
                  objectFit: "cover", 
                  objectPosition: "center top", // Show the top part of the image
                  width: "100%", 
                  height: "100%"
                }}
              />
            </div>
            <CardBody>
              <h5 className="card-title">{product.name}</h5>
              <p className="card-text">{product.description}</p>
            </CardBody>
            <CardFooter className="bg-white d-flex justify-content-between align-items-center" style={{ borderBottomLeftRadius: "15px", borderBottomRightRadius: "15px" }}>
              <strong>{product.points_cost} MEOS</strong>
              {product.available ? (
                <Badge color="success">Available</Badge>
              ) : (
                <Badge color="danger">Unavailable</Badge>
              )}
            </CardFooter>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default ProductDetails;

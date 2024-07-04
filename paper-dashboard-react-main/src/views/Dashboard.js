import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Card, CardBody, CardFooter, Row, Col, Badge } from "reactstrap";
import { CSSTransition, TransitionGroup } from "react-transition-group";
import './transitions.css'; // Import the CSS file for transitions

function Dashboard() {
  const [products, setProducts] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const hostname = window.location.hostname;
    const baseUrl = hostname === 'localhost' ? 'http://localhost' : `http://${hostname}`;

    fetch(`${baseUrl}/api/scrape_data/`)
      .then(response => response.json())
      .then(data => setProducts(data))
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  const handleCardClick = (id) => {
    navigate(`/admin/product-details/${id}`);
  };

  return (
    <>
      <div className="content">
        <TransitionGroup component={Row}>
          {products.map((product) => (
            <CSSTransition
              key={product.id}
              timeout={300}
              classNames="fade"
            >
              <Col lg="3" md="6" sm="6" className="mb-4">
                <Card 
                  className="h-100" 
                  onClick={() => handleCardClick(product.id)} 
                  style={{ 
                    cursor: "pointer", 
                    borderRadius: "15px" // Rounded corners
                  }}
                >
                  <div className="card-img-top-wrapper" style={{ height: "200px", overflow: "hidden", borderTopLeftRadius: "15px", borderTopRightRadius: "15px" }}>
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
                    <p className="card-text small text-muted">{product.description}</p>
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
            </CSSTransition>
          ))}
        </TransitionGroup>
      </div>
    </>
  );
}

export default Dashboard;

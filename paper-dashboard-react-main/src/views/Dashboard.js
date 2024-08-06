import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Card, CardBody, CardFooter, Row, Col, Badge, ButtonGroup, Button } from "reactstrap";
import { CSSTransition, TransitionGroup } from "react-transition-group";
import './transitions.css'; // Import the CSS file for transitions

function Dashboard() {
  const [products, setProducts] = useState([]);
  const [filteredProducts, setFilteredProducts] = useState([]);
  const [filter, setFilter] = useState('all'); // 'all', 'available', or 'unavailable'
  const navigate = useNavigate();

  useEffect(() => {
    const hostname = window.location.hostname;
    const baseUrl = hostname === 'localhost' ? 'http://localhost' : `http://${hostname}`;

    fetch(`${baseUrl}/api/scrape_data/`)
      .then(response => response.json())
      .then(data => {
        setProducts(data);
        setFilteredProducts(data);
      })
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  useEffect(() => {
    let filtered;
    switch(filter) {
      case 'available':
        filtered = products.filter(product => product.available);
        break;
      case 'unavailable':
        filtered = products.filter(product => !product.available);
        break;
      default:
        filtered = products;
    }
    setFilteredProducts(filtered);
  }, [filter, products]);

  const handleCardClick = (id) => {
    navigate(`/admin/product-details/${id}`);
  };

  return (
    <>
      <div className="content">
        <div className="filter-container" style={{ marginBottom: '20px' }}>
          <ButtonGroup size="sm">
            <Button 
              color={filter === 'all' ? 'primary' : 'secondary'}
              onClick={() => setFilter('all')}
            >
              All
            </Button>
            <Button 
              color={filter === 'available' ? 'primary' : 'secondary'}
              onClick={() => setFilter('available')}
            >
              Available
            </Button>
            <Button 
              color={filter === 'unavailable' ? 'primary' : 'secondary'}
              onClick={() => setFilter('unavailable')}
            >
              Unavailable
            </Button>
          </ButtonGroup>
        </div>
        <TransitionGroup component={Row}>
          {filteredProducts.map((product) => (
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
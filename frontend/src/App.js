import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.css';
import { Container, Form, Button, ListGroup } from 'react-bootstrap';

const App = () => {
  const [groups, setGroups] = useState([]);
  const [selectedGroup, setSelectedGroup] = useState('');
  const [updatedGroupName, setUpdatedGroupName] = useState('');
  const [updatedGroupOwner, setUpdatedGroupOwner] = useState('');
  const [newGroupName, setNewGroupName] = useState('');
  const [newGroupOwner, setNewGroupOwner] = useState('');

  useEffect(() => {
    fetch('http://127.0.0.1:5000/group')
      .then(response => response.json())
      .then(data => setGroups(data));
  }, []);

  const createGroup = async (event) => {
    event.preventDefault();

    await fetch('http://127.0.0.1:5000/group', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: newGroupName,
        owner: newGroupOwner
      })
    });

    // Reload groups from the server
    const response = await fetch('http://127.0.0.1:5000/group');
    const data = await response.json();
    setGroups(data);
  };

  const updateGroup = async (event) => {
    event.preventDefault();

    await fetch(`http://127.0.0.1:5000/group/${selectedGroup}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: updatedGroupName,
        owner: updatedGroupOwner
      })
    });

    // Reload groups from the server
    const response = await fetch('http://127.0.0.1:5000/group');
    const data = await response.json();
    setGroups(data);
  };

  return (
    <Container>
      <h2>Create Group</h2>
      <Form onSubmit={createGroup}>
        <Form.Group controlId="newGroupName">
          <Form.Label>Group Name</Form.Label>
          <Form.Control type="text" value={newGroupName} onChange={e => setNewGroupName(e.target.value)} />
        </Form.Group>
        <Form.Group controlId="newGroupOwner">
          <Form.Label>Group Owner</Form.Label>
          <Form.Control type="text" value={newGroupOwner} onChange={e => setNewGroupOwner(e.target.value)} />
        </Form.Group>
        <Button variant="primary" type="submit">Create Group</Button>
      </Form>
      <h2>Update Group</h2>
      <Form onSubmit={updateGroup}>
        <Form.Group controlId="selectedGroup">
          <Form.Label>Group ID</Form.Label>
          <Form.Control type="number" value={selectedGroup} onChange={e => setSelectedGroup(e.target.value)} />
        </Form.Group>
        <Form.Group controlId="updatedGroupName">
          <Form.Label>New Group Name</Form.Label>
          <Form.Control type="text" value={updatedGroupName} onChange={e => setUpdatedGroupName(e.target.value)} />
        </Form.Group>
        <Form.Group controlId="updatedGroupOwner">
          <Form.Label>New Group Owner</Form.Label>
          <Form.Control type="text" value={updatedGroupOwner} onChange={e => setUpdatedGroupOwner(e.target.value)} />
        </Form.Group>
        <Button variant="primary" type="submit">Update Group</Button>
      </Form>
      <hr />
      <h2>Groups</h2>
      <ListGroup>
      {groups.map(group => (
        <ListGroup.Item key={group.id}>
          <h3>{group.name}</h3>
          <p>Owner: {group.owner}</p>
          <p>Created At: {new Date(group.createdAt).toLocaleString()}</p>
        </ListGroup.Item>
      ))}
      </ListGroup>
    </Container>
  );
};

export default App;

package message

import (
	"encoding/json"
	"fmt"

	"github.com/orcalabs/plugin-sdk/go/plugin/parameter"
)

// Dispatchable is an interface to be able to be disptached to the queue
type Dispatchable interface {
	Dispatch(url string) error
}

// Message contains general message information that other messages should embed
type Message struct {
	Header // Message header
	Body   // Message body
}

// Validate the msg against the provided msgtype.
func (m *Message) Validate() error {
	if m.Version != Version {
		return fmt.Errorf("Unexpected version, wanted: %s but got %s", Version, m.Version)
	}
	return nil
}

// Marshal marshals a Message object into JSON
func (m *Message) Marshal(v interface{}) ([]byte, error) {
	bodyBytes, err := m.Body.MarshalJSON()
	if err != nil {
		return nil, err
	}
	m.Body.RawMessage = bodyBytes
	return json.Marshal(&m)
}

// Unmarshal unmarshals a Message object
func (m *Message) Unmarshal(body interface{}) error {
	if err := parameter.Unmarshal(&m); err != nil {
		return err
	}

	if err := m.Validate(); err != nil {
		return err
	}

	if err := m.UnmarshalBody(body); err != nil {
		return fmt.Errorf("Unable to marshal Message.Body: %+v", err)
	}

	return nil
}

// UnmarshalBody unmarshalls a Body object
func (m *Message) UnmarshalBody(body interface{}) error {
	err := json.Unmarshal(m.Body.RawMessage, body)
	if err != nil {
		return fmt.Errorf("Unable to unmarshal Body: %+v", err)
	}
	return nil
}
package plugin

// Actionable must be implemented by Actions to work with Plugins
type Actionable interface {
	Act() error   // Act will run the action.
	Name() string // Name is the name of the action
}

// Action defines a struct that should be embedded within any
// implemented Action.
type Action struct {
	name string
}

// Init initializes the action with the action name.
func (t *Action) Init(name string) {
	t.name = name
}

// Name of  the action
func (t *Action) Name() string {
	return t.name
}

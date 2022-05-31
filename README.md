# Robot Factory

A small CLI based RPG to experiment with different combat systems.

## Combat

Combat works by each robot taking turns to carry out an action. Actions are not carried out strictly one after the other, rather there is a cooldown required between actions, and this is linked to a base speed of the robot, plus any modifiers resulting from previous actions or other effects (e.g. damage etc)

Combat is over when an entire team is either disabled or destroyed.
- Destroyed: All components have been destroyed (reduced to 0 HP)
- Disabled: No actions are available. Components have either been destroyed or require stats which are too low (and unrecoverable).

## Action Types

There are eight types of actions to account for in terms of what they affect:
- Offensive : Single Target - Single Component e.g. Direct Stab Attack 
- Offensive : Single Target - Multiple Components e.g. Splash Damage
- Offensive : Single Target - All Components e.g. EMP
- Offensive : Single Target - Global e.g. A global effect such as Charge Drain
- Defensive : Single Source - Single Component e.g. Repair
- Defensive : Single Source - Multiple Components e.g. Enhance
- Defensive : Single Source - All Components e.g. 

In the future this could be expanded for Multiple Source/Target - All Components/Global etc.

## Components

Robots are comprised of a series of components, and components are key to the combat system. Each component has its own independant stats which aggregate together to form the overall robots stats.

Components are loaded into the game via the file, which has a (somewhat crude) flat text file format.

0   : ComponentType
1   : ComponentName
2   : HP DEF CRG PRE 
3-n : ActionType["A","P"] ActionName EffectType Args .. ConstraintType Args ... 

Components are categories into the following roles which indicates what they are used for:
- Weapon 
- Item Storage
- Repair
- Movement
- Charge Storage
- Charge Generation
- Pressure Generation
- Water Storage

## Inventory/Items

Items can be used to for a variety of reasons. The following types of items exist:
- Currency: Used for purchasing other items etc.
- Stat Upgrades (Permanent): Permanently improve a robots stats. Consumable.
- Stat Upgrades (Temporary): Temporarily improve a robots stats. Consumable.
- Upgrade Parts: Upgrade parts are used towards upgrading specific components.
- Components: Full components that can be equipped.
- Combat: Has either active/passive effects which are available in combat.

Items are carried by robots in dedicated components. This means that if those components are destroyed, the items within are lost. Items which can be used in combat are exposed as active/passive actions for the component storing them.

Examples of these components:
- Box
- Container
- Chest

## Discipline Types

There are four main disciplines:
- Electric
- Steam
- Clockwork
- Alchemy

Each discipline has certain traits and characteristics which present themselves throughout components which follow them. They also dictate a strength/weakness cycle to allow for interesting countering.

### Electric

Components use charge, can be regenerated and stored. Components are disabled if not enough charge.
Depending on generator, either renewable (solar) or consumable (wood/coal)

- Weak vs Clockwork, Strong vs Steam

### Steam

Components require a minimum pressure level to be used however pressure is not lost when those components are used. Boilers provide a level of pressure and consume water (and potentially other fuels) constantly, irrespective of whether the steam is used. If a boiler is destroyed or runs out of water/fuel then that pressure level is lost and components may cease to work.

- Weak vs Electric, Strong vs Clockwork

### Clockwork

Components don't need any consumable to operate, however they benefit from "clockwork" e.g. gears/cogs etc which reduce their cooldown. The more clockwork a robot has, the faster it can execute its actions. Clockwork robots also have a lot of passive actions that do damage, as they are timing based/periodic.

### Alchemy


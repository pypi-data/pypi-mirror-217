//===- Var.h ----------------------------------------------------*- C++ -*-===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//

#ifndef MLIR_DIALECT_SPARSETENSOR_IR_DETAIL_VAR_H
#define MLIR_DIALECT_SPARSETENSOR_IR_DETAIL_VAR_H

#include "TemplateExtras.h"

#include "mlir/IR/OpImplementation.h"
#include "llvm/ADT/EnumeratedArray.h"
#include "llvm/ADT/SmallBitVector.h"
#include "llvm/ADT/StringMap.h"

namespace mlir {
namespace sparse_tensor {
namespace ir_detail {

// Throughout this namespace we use the name `isWF` (is "well-formed")
// for predicates that detect intrinsic structural integrity criteria,
// and hence which should always be assertively true.  Whereas we reserve
// the name `isValid` for predicates that detect extrinsic semantic
// integrity criteria, and hence which may legitimately return false even
// in well-formed programs.  Moreover, "validity" is often a relational
// or contextual property, and therefore the same term may be considered
// valid in one context yet invalid in another.
//
// As an example of why we make this distinction, consider `Var`.
// A variable is well-formed if its kind and identifier are both well-formed;
// this can be checked locally, and the resulting truth-value holds globally.
// Whereas, a variable is valid with respect to a particular `Ranks` only if
// it is within bounds; and a variable is valid with respect to a particular
// `DimLvlMap` only if the variable is bound and all uses of the variable
// are within the scope of that binding.

// Throughout this namespace we use `enum class` types to form "newtypes".
// The enum-based implementation of newtypes only serves to block implicit
// conversions; it cannot enforce any wellformedness constraints, since
// `enum class` permits using direct-list-initialization to construct
// arbitrary values[1].  Consequently, we use the syntax "`E{u}`" whenever
// we intend that ctor to be a noop (i.e., `std::is_same_v<decltype(u),
// std::underlying_type_t<E>>`), since the compiler will ensure that that's
// the case.  Whereas we only use the "`static_cast<E>(u)`" syntax when we
// specifically intend to introduce conversions.
//
// [1]:
// <https://en.cppreference.com/w/cpp/language/enum#enum_relaxed_init_cpp17>

//===----------------------------------------------------------------------===//
/// The three kinds of variables that `Var` can be.
///
/// NOTE: The numerical values used to represent this enum should be
/// treated as an implementation detail, not as part of the API.  In the
/// API below we use the canonical ordering `{Symbol,Dimension,Level}` even
/// though that does not agree with the numerical ordering of the numerical
/// representation.
enum class VarKind { Symbol = 1, Dimension = 0, Level = 2 };

constexpr bool isWF(VarKind vk) {
  const auto vk_ = to_underlying(vk);
  return 0 <= vk_ && vk_ <= 2;
}

/// Swaps `Dimension` and `Level`, but leaves `Symbol` the same.
constexpr VarKind flipVarKind(VarKind vk) {
  return VarKind{2 - to_underlying(vk)};
}
static_assert(flipVarKind(VarKind::Symbol) == VarKind::Symbol &&
              flipVarKind(VarKind::Dimension) == VarKind::Level &&
              flipVarKind(VarKind::Level) == VarKind::Dimension);

/// Gets the ASCII character used as the prefix when printing `Var`.
constexpr char toChar(VarKind vk) {
  // If `isWF(vk)` then this computation's intermediate results are always
  // in the range [-44..126] (where that lower bound is under worst-case
  // rearranging of the expression); and `int_fast8_t` is the fastest type
  // which can support that range without over-/underflow.
  const auto vk_ = static_cast<int_fast8_t>(to_underlying(vk));
  return static_cast<char>(100 + vk_ * (26 - vk_ * 11));
}
static_assert(toChar(VarKind::Symbol) == 's' &&
              toChar(VarKind::Dimension) == 'd' &&
              toChar(VarKind::Level) == 'l');

//===----------------------------------------------------------------------===//
/// The type of arrays indexed by `VarKind`.
template <typename T>
using VarKindArray = llvm::EnumeratedArray<T, VarKind, VarKind::Level>;

//===----------------------------------------------------------------------===//
/// A concrete variable, to be used in our variant of `AffineExpr`.
class Var {
public:
  /// Typedef to help disambiguate different uses of `unsigned`.
  using Num = unsigned;

private:
  /// The underlying storage representation of `Var`.  Note that this type
  /// should be kept distinct from `Num`.  Not only can they be different
  /// C++ types (even though they currently happen to be the same), but
  /// they also use different bitwise representations.
  //
  // FUTURE_CL(wrengr): Rather than rolling our own, we should
  // consider using "llvm/ADT/Bitfields.h"; though that seems to only
  // be used by LLVM for the sake of defining machine/assembly ops.
  // Or we could consider abusing `PointerIntPair`...
  using Impl = unsigned;
  Impl impl;

  /// The largest `Var::Num` supported by `Var::Impl`.  Two low-order
  /// bits are reserved for storing the `VarKind`, and one high-order bit
  /// is reserved for future use (e.g., to support `DenseMapInfo<Var>` while
  /// maintaining the usual numeric values for "empty" and "tombstone").
  static constexpr Num kMaxNum =
      static_cast<Num>(std::numeric_limits<Impl>::max() >> 3);

public:
  // This must be public for `VarInfo` to use it (whereas we don't want
  // to expose the `impl` field via friendship).
  static constexpr bool isWF_Num(Num n) { return n <= kMaxNum; }

  constexpr Var(VarKind vk, Num n)
      : impl((static_cast<Impl>(n) << 2) |
             static_cast<Impl>(to_underlying(vk))) {
    assert(isWF(vk) && "unknown VarKind");
    assert(isWF_Num(n) && "Var::Num is too large");
  }
  Var(AffineSymbolExpr sym) : Var(VarKind::Symbol, sym.getPosition()) {}
  Var(VarKind vk, AffineDimExpr var) : Var(vk, var.getPosition()) {}

  constexpr bool operator==(Var other) const { return impl == other.impl; }
  constexpr bool operator!=(Var other) const { return !(*this == other); }

  constexpr VarKind getKind() const { return static_cast<VarKind>(impl & 3); }
  constexpr Num getNum() const { return static_cast<Num>(impl >> 2); }

  template <typename U>
  constexpr bool isa() const;
  template <typename U>
  constexpr U cast() const;
  template <typename U>
  constexpr U dyn_cast() const;

  void print(llvm::raw_ostream &os) const;
  void print(AsmPrinter &printer) const;
  void dump() const;
};
static_assert(IsZeroCostAbstraction<Var>);

class SymVar final : public Var {
public:
  static constexpr VarKind Kind = VarKind::Symbol;
  static constexpr bool classof(Var const *var) {
    return var->getKind() == Kind;
  }
  constexpr SymVar(Num sym) : Var(Kind, sym) {}
  SymVar(AffineSymbolExpr symExpr) : Var(symExpr) {}
};
static_assert(IsZeroCostAbstraction<SymVar>);

// TODO(wrengr): I'd like to give the ctors the types `DimVar(Dimension)`
// and `LvlVar(Level)`, instead of their current types using `Num`;
// however, that'd require importing "IR/SparseTensor.h" which nothing else
// in this file requires.  Also beware the issues about implicit-conversion
// from `uint64_t` to `Num`.
class DimVar final : public Var {
public:
  static constexpr VarKind Kind = VarKind::Dimension;
  static constexpr bool classof(Var const *var) {
    return var->getKind() == Kind;
  }
  constexpr DimVar(Num dim) : Var(Kind, dim) {}
  DimVar(AffineDimExpr dimExpr) : Var(Kind, dimExpr) {}
};
static_assert(IsZeroCostAbstraction<DimVar>);

class LvlVar final : public Var {
public:
  static constexpr VarKind Kind = VarKind::Level;
  static constexpr bool classof(Var const *var) {
    return var->getKind() == Kind;
  }
  constexpr LvlVar(Num lvl) : Var(Kind, lvl) {}
  LvlVar(AffineDimExpr lvlExpr) : Var(Kind, lvlExpr) {}
};
static_assert(IsZeroCostAbstraction<LvlVar>);

// FIXME(wrengr): In order to get the `llvm::{isa,cast,dyn_cast}`
// free-functions to work (instead of using our hand-rolled methods),
// we'll need to define something like this:
// ```
// namespace llvm {
// template <typename U> struct CastInfo<U, Var> : OptionalValueCast<U, Var> {};
// template <> struct ValueIsPresent<Var> {
//   using UnwrappedType = Var;
//   static inline bool isPresent(Var const&) { return true; }
// };
// } // namespace llvm
// ```
// The above will enable the type `llvm::dyn_cast<U>(Var) -> std::optional<U>`.
//
// FIXME(wrengr): The default `OptionalValueCast<U,Var>::doCast(Var const&)`
// implementation uses the expression "`U(var)`", which means that all the
// subclasses will need to define that upcasting-copy-ctor, and to ensure
// safety/correctness will need to mark that ctor as private/protected,
// which in turn means they'll need make the `CastInfo`/`OptionalValueCast`
// classes friends.
//
// We run into similar issues with our hand-rolled methods, the only
// difference is that the upcasting-copy-ctor would have type `U(Impl)`
// instead of `U(Var)` and that we'd need to make the `Var` class a friend
// rather than the `CastInfo`/`OptionalValueCast` classes.
//
template <typename U>
constexpr bool Var::isa() const {
  if constexpr (std::is_same_v<U, SymVar>)
    return getKind() == VarKind::Symbol;
  if constexpr (std::is_same_v<U, DimVar>)
    return getKind() == VarKind::Dimension;
  if constexpr (std::is_same_v<U, LvlVar>)
    return getKind() == VarKind::Level;
  // NOTE: The `AffineExpr::isa` implementation doesn't have a fallthrough
  // case returning `false`; wrengr guesses that's so things will fail
  // to compile whenever `!std::is_base_of<Var, U>`.  Though it's unclear
  // why they implemented it that way rather than using SFINAE for that,
  // especially since it would give better error messages.
}

template <typename U>
constexpr U Var::cast() const {
  assert(isa<U>());
  return U(impl >> 2); // NOTE TO Wren: confirm this fix
}

template <typename U>
constexpr U Var::dyn_cast() const {
  return isa<U>() ? U(impl >> 2) : U();
}

//===----------------------------------------------------------------------===//
// Forward-decl so that we can declare methods of `Ranks` and `VarSet`.
class DimLvlExpr;

//===----------------------------------------------------------------------===//
class Ranks final {
  // Not using `VarKindArray` since `EnumeratedArray` doesn't support constexpr.
  // TODO(wrengr): to what extent do we actually care about constexpr here?
  unsigned impl[3];

  static constexpr unsigned to_index(VarKind vk) {
    assert(isWF(vk) && "unknown VarKind");
    return static_cast<unsigned>(to_underlying(vk));
  }

public:
  // NOTE_TO_SELF(wrengr): According to <https://stackoverflow.com/a/34465458>
  // we should be able to do this just fine, even though `constexpr`
  constexpr Ranks(unsigned symRank, unsigned dimRank, unsigned lvlRank)
      : impl() {
    impl[to_index(VarKind::Symbol)] = symRank;
    impl[to_index(VarKind::Dimension)] = dimRank;
    impl[to_index(VarKind::Level)] = lvlRank;
  }
  Ranks(VarKindArray<unsigned> const &ranks)
      : Ranks(ranks[VarKind::Symbol], ranks[VarKind::Dimension],
              ranks[VarKind::Level]) {}

  constexpr unsigned getRank(VarKind vk) const { return impl[to_index(vk)]; }
  constexpr unsigned getSymRank() const { return getRank(VarKind::Symbol); }
  constexpr unsigned getDimRank() const { return getRank(VarKind::Dimension); }
  constexpr unsigned getLvlRank() const { return getRank(VarKind::Level); }

  constexpr bool isValid(Var var) const {
    return var.getNum() < getRank(var.getKind());
  }
  bool isValid(DimLvlExpr expr) const;
};
static_assert(IsZeroCostAbstraction<Ranks>);

//===----------------------------------------------------------------------===//
class VarSet final {
  // If we're willing to give up the possibility of resizing the
  // individual bitvectors, then we could flatten this into a single
  // bitvector (akin to how `mlir::presburger::PresburgerSpace` does it);
  // however, doing so would greatly complicate the implementation of the
  // `occursIn(VarSet)` method.
  VarKindArray<llvm::SmallBitVector> impl;

public:
  explicit VarSet(Ranks const &ranks);

  // TODO(wrengr): can we come up with a single name that works for all three of
  // these?
  bool contains(Var var) const;
  bool occursIn(VarSet const &vars) const;
  bool occursIn(DimLvlExpr expr) const;

  void add(Var var);
  // TODO(wrengr): void add(VarSet const& vars);
  void add(DimLvlExpr expr);
};

//===----------------------------------------------------------------------===//
// TODO(wrengr): For good error messages we'll need to define something like:
// ```class LocatedVar final { llvm::SMLoc loc; VarInfo::ID id; };```
// to be the actual thing occuring in our variant of AffineExpr.
// Though we may also want that struct to contain a pointer back to the
// `VarEnv` which contains the `VarInfo` for that `VarInfo::ID`.
//
// To go along with this, the `VarInfo` record should drop its own `SMLoc`
// field.

//===----------------------------------------------------------------------===//
/// A record of metadata for/about a variable, used by `VarEnv`.
/// The principal goal of this record is to enable `VarEnv` to be used for
/// incremental parsing; in particular, `VarInfo` allows the `Var::Num` to
/// remain unknown, since each record is instead identified by `VarInfo::ID`.
/// Therefore the `VarEnv` can freely allocate `VarInfo::ID` in whatever
/// order it likes, irrespective of the binding order (`Var::Num`) of the
/// associated variable.
class VarInfo final {
public:
  /// Newtype for unique identifiers of `VarInfo` records, to ensure
  /// they aren't confused with `Var::Num`.
  enum class ID : unsigned {};

private:
  // FUTURE_CL(wrengr): We could use the high-bit of `Var::Impl` to
  // store the `std::optional` bit, therefore allowing us to bitbash the
  // `num` and `kind` fields together.
  //
  StringRef name;              // The bare-id used in the MLIR source.
  llvm::SMLoc loc;             // The location of the first occurence.
                               // TODO(wrengr): See the above `LocatedVar` note.
  ID id;                       // The unique `VarInfo`-identifier.
  std::optional<Var::Num> num; // The unique `Var`-identifier (if resolved).
  VarKind kind;                // The kind of variable.

public:
  constexpr VarInfo(ID id, StringRef name, llvm::SMLoc loc, VarKind vk,
                    std::optional<Var::Num> n = {})
      : name(name), loc(loc), id(id), num(n), kind(vk) {
    assert(!name.empty() && "null StringRef");
    assert(isWF(vk) && "unknown VarKind");
    assert((!n || Var::isWF_Num(*n)) && "Var::Num is too large");
    // NOTE TO Wren: windows did not like loc.isValid constexpr
  }

  constexpr StringRef getName() const { return name; }
  constexpr llvm::SMLoc getLoc() const { return loc; }
  Location getLocation(AsmParser &parser) const {
    return parser.getEncodedSourceLoc(loc);
  }
  constexpr ID getID() const { return id; }
  constexpr VarKind getKind() const { return kind; }
  constexpr std::optional<Var::Num> getNum() const { return num; }
  constexpr bool hasNum() const { return num.has_value(); }
  void setNum(Var::Num n);
  constexpr Var getVar() const {
    assert(hasNum());
    return Var(kind, *num);
  }
  constexpr std::optional<Var> tryGetVar() const {
    return num ? std::make_optional(Var(kind, *num)) : std::nullopt;
  }
};
// We don't actually require this, since `VarInfo` is a proper struct
// rather than a newtype.  But it passes, so for now we'll keep it around.
static_assert(IsZeroCostAbstraction<VarInfo>);

//===----------------------------------------------------------------------===//
enum class CreationPolicy { MustNot, May, Must };

class VarEnv final {
  /// Map from `VarKind` to the next free `Var::Num`; used by `bindVar`.
  VarKindArray<Var::Num> nextNum;
  /// Map from `VarInfo::ID` to shared storage for the actual `VarInfo` objects.
  SmallVector<VarInfo> vars;
  /// Map from variable names to their `VarInfo::ID`.
  llvm::StringMap<VarInfo::ID> ids;

  VarInfo::ID nextID() const { return static_cast<VarInfo::ID>(vars.size()); }

public:
  // NOTE TO Wren: initializer needed!
  VarEnv() : nextNum(0) {}

  /// Gets the underlying storage for the `VarInfo` identified by
  /// the `VarInfo::ID`.
  ///
  /// NOTE: The returned reference can become dangling if the `VarEnv`
  /// object is mutated during the lifetime of the pointer.  Therefore,
  /// client code should not store the reference nor otherwise allow it
  /// to live too long.
  //
  // FUTURE_CL(wrengr): Consider trying to define/use a nested class
  // `struct{VarEnv*; VarInfo::ID}` akin to `BitVector::reference`.
  VarInfo const &access(VarInfo::ID id) const {
    // `SmallVector::operator[]` already asserts the index is in-bounds.
    return vars[to_underlying(id)];
  }
  VarInfo const *access(std::optional<VarInfo::ID> oid) const {
    return oid ? &access(*oid) : nullptr;
  }

  Var toVar(VarInfo::ID id) const { return vars[to_underlying(id)].getVar(); }

private:
  VarInfo &access(VarInfo::ID id) {
    return const_cast<VarInfo &>(std::as_const(*this).access(id));
  }
  VarInfo *access(std::optional<VarInfo::ID> oid) {
    return const_cast<VarInfo *>(std::as_const(*this).access(oid));
  }

public:
  /// Attempts to look up the variable with the given name.
  std::optional<VarInfo::ID> lookup(StringRef name) const;

  /// Attempts to create a new currently-unbound variable.  When a variable
  /// of that name already exists: if `verifyUsage` is true, then will assert
  /// that the variable has the same kind and a consistent location; otherwise,
  /// when `verifyUsage` is false, this is a noop.  Returns the identifier
  /// for the variable with the given name (i.e., either the newly created
  /// variable, or the pre-existing variable), and a bool indicating whether
  /// a new variable was created.
  std::pair<VarInfo::ID, bool> create(StringRef name, llvm::SMLoc loc,
                                      VarKind vk, bool verifyUsage = false);

  /// Attempts to lookup or create a variable according to the given
  /// `CreationPolicy`.  Returns nullopt in one of two circumstances:
  /// (1) the policy says we `Must` create, yet the variable already exists;
  /// (2) the policy says we `MustNot` create, yet no such variable exists.
  /// Otherwise, if the variable already exists then it is validated against
  /// the given kind and location to ensure consistency.
  //
  // TODO(wrengr): Define an enum of error codes, to avoid `nullopt`-blindness
  // TODO(wrengr): Prolly want to rename this to `create` and move the
  // current method of that name to being a private `createImpl`.
  std::optional<std::pair<VarInfo::ID, bool>>
  lookupOrCreate(CreationPolicy policy, StringRef name, llvm::SMLoc loc,
                 VarKind vk);

  /// Binds the given variable to the next free `Var::Num` for its `VarKind`.
  Var bindVar(VarInfo::ID id);

  /// Creates a new variable of the given kind and immediately binds it.
  /// This should only be used whenever the variable is known to be unused
  /// and therefore does not have a name.
  Var bindUnusedVar(VarKind vk);

  InFlightDiagnostic emitErrorIfAnyUnbound(AsmParser &parser) const;

  Ranks getRanks() const { return Ranks(nextNum); }
};

//===----------------------------------------------------------------------===//

} // namespace ir_detail
} // namespace sparse_tensor
} // namespace mlir

#endif // MLIR_DIALECT_SPARSETENSOR_IR_DETAIL_VAR_H

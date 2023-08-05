/* Copyright 2023 The TensorFlow Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

#ifndef TENSORFLOW_COMPILER_MLIR_QUANTIZATION_STABLEHLO_PASSES_BRIDGE_PASSES_H_
#define TENSORFLOW_COMPILER_MLIR_QUANTIZATION_STABLEHLO_PASSES_BRIDGE_PASSES_H_

#include <memory>

#define GEN_PASS_DECL
#include "mlir/Dialect/Func/IR/FuncOps.h"  // from @llvm-project
#include "mlir/Pass/Pass.h"  // from @llvm-project

namespace mlir {
namespace stablehlo {

// Legalizes from MHLO quantized ops with MHLO quant types to MHLO primitive ops
// like int ops.
std::unique_ptr<OperationPass<func::FuncOp>> createConvertMHLOQuantToIntPass(
    bool legalize_chlo = true);

#define GEN_PASS_REGISTRATION
#define GEN_PASS_DECL_CONVERTMHLOQUANTTOINT
#include "tensorflow/compiler/mlir/quantization/stablehlo/passes/bridge/passes.h.inc"

}  // namespace stablehlo
}  // namespace mlir

#endif  // TENSORFLOW_COMPILER_MLIR_QUANTIZATION_STABLEHLO_PASSES_BRIDGE_PASSES_H_
